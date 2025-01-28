from inspect import getsourcefile
from random import randint
from requests import post
from loguru import logger
from time import sleep
from tqdm import tqdm
import sys
import ctypes
import os
sys.__stdout__ = sys.stdout

TG_BOT_TOKEN = '' # токен от тг бота (`12345:Abcde`) для уведомлений. если не нужно - оставляй пустым
TG_USER_ID = [] # тг айди куда должны приходить уведомления. [21957123] - для отправления уведомления только себе, [21957123, 103514123] - отправлять нескольким людями

windll = ctypes.windll if os.name == 'nt' else None # for Mac users


class WindowName:
    def __init__(self):
        try: self.path = os.path.abspath(getsourcefile(lambda: 0)).split("\\")[-2]
        except: self.path = os.path.abspath(getsourcefile(lambda: 0)).split("/")[-2]

        self.accs_done = 0
        self.modules_amount = 0
        self.modules_done = 0

    def update_accs(self):
        self.accs_done += 1
        self.modules_amount = 0
        self.modules_done = 0

    def update_modules(self):
        self.modules_done += 1

    def set_modules(self, modules_amount: int):
        self.modules_amount = modules_amount


class TgReport:
    def __init__(self):
        self.logs = ''


    def update_logs(self, text: str):
        self.logs += f'{text}\n'


    def send_log(self, wallet, window_name, mode: str):
        notification_text = f'[{window_name.accs_done}/{window_name.accs_amount}] <i>{wallet.address}</i>\n\n' \
                            f'{self.logs}\n'
        if mode == 'Claim quests': notification_text += f'{wallet.stats.get("status")}'

        texts = []
        while len(notification_text) > 0:
            texts.append(notification_text[:1900])
            notification_text = notification_text[1900:]

        if TG_BOT_TOKEN:
            for tg_id in TG_USER_ID:
                for text in texts:
                    try: post(f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?parse_mode=html&chat_id={tg_id}&text={text}')
                    except Exception as err: logger.error(f'[-] TG | Send Telegram message error to {tg_id}: {err}')


def sleeping(*timing):
    if type(timing[0]) == list: timing = timing[0]
    if len(timing) == 2: x = randint(timing[0], timing[1])
    else: x = timing[0]
    for _ in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        sleep(1)


def make_text_border(text: str):
    new_text = ''
    max_len = max([len(string) for string in text.split('\n')])

    new_text += '+' + '-' * (max_len + 8) + '+\n'
    for string in text.split('\n'): new_text += f'\t{string}\n'
    new_text += '+' + '-' * (max_len + 8) + '+\n'

    return new_text
