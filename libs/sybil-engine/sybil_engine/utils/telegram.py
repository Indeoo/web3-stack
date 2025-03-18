import telebot
from loguru import logger

from sybil_engine.utils.config_utils import get_config
from sybil_engine.utils.utils import ConfigurationException


def send_to_bot(msg):
    if get_config("telegram_api_key") is None or get_config("telegram_api_chat_id") is None:
        raise ConfigurationException('telegram api key and chat id should be configured if telegram is on')
    try:
        bot = telebot.TeleBot(get_config("telegram_api_key"))
        bot.send_message(get_config("telegram_api_chat_id"), msg)
    except Exception as error:
        logger.error(f"Fail to send {msg} {error}")


