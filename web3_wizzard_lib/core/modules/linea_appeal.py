import random
import webbrowser

from loguru import logger
from sybil_engine.module.module import Module
from sybil_engine.utils.accumulator import add_accumulator, get_value
from sybil_engine.utils.statistic_utils import get_statistic_writer, statistic_date_string

from web3_wizzard_lib.core.utils.ai_utils import get_ai_chat
from sybil_engine.utils.telegram import add_config

from web3_wizzard_lib.core.utils.module_memory import get_by_key, accumulate_by_key, remove_key

APPEAL_ACCOUNTS = "APPEAL_ACCOUNTS"
APPEAL_ACCOUNTS_AMOUNT = "APPEAL_ACCOUNTS_AMOUNT"


class LineaAppeal(Module):
    module_name = 'LINEA_APPEAL'
    module_config = "linea_appeal_config"
    base_url = "https://docs.google.com/forms/d/e/1FAIpQLSfkbHzC1hZTy6u5R8S5i6wQ2xCyUZQjvucmlyChwg04fJIO5Q/viewform"

    with open("resources/linea_appeal.txt") as f:
        linea_appeal_reason = f.read()

    def execute(self, token, accounts, statistic_write, ai_type, account):
        add_accumulator("Acc Num", 1)

        statistics = get_statistic_writer()
        statistics.init_if_required(
            statistic_date_string,
            ["#", "MainAddress", "GPT Answer"]
        )

        chat_gpt = get_ai_chat(ai_type, token)
        reason = chat_gpt.ask(self.linea_appeal_reason)
        logger.info(reason)

        statistics.write_row(
            statistic_date_string,
            [account.app_id, account.address, reason]
        )

        if not get_by_key(APPEAL_ACCOUNTS_AMOUNT):
            add_config(
                APPEAL_ACCOUNTS_AMOUNT,
                random.randint(accounts['from'], accounts['to'])
            )

        accumulate_by_key(
            APPEAL_ACCOUNTS, {
                "address": account.address,
                "reason": reason,
            }
        )

        if (get_by_key(APPEAL_ACCOUNTS_AMOUNT) == len(get_by_key(APPEAL_ACCOUNTS))
                or get_value("Acc Num") == get_value("Acc Amount")):
            wallets = get_by_key(APPEAL_ACCOUNTS)
            address_list = [wallet["address"] for wallet in wallets]
            formatted_string = "\n".join(f"{wallet['address']}\n{wallet['reason']}" for wallet in wallets)
            self.open_appeal_form(account, address_list, formatted_string)
            remove_key(APPEAL_ACCOUNTS)
            remove_key(APPEAL_ACCOUNTS_AMOUNT)

    def open_appeal_form(self, account, address_list, formatted_string):
        payload = {
            "entry.1292139045": account.address,
            "entry.1099559693": address_list,
            "entry.1296389817": formatted_string
        }
        query_string = "&".join(f"{key}={value}" for key, value in payload.items())
        pre_filled_url = f"{self.base_url}?{query_string}"
        print(f"Opening form: {pre_filled_url}")
        webbrowser.open(pre_filled_url)

    def parse_params(self, module_params):
        return (
            module_params['ai_token'],
            module_params['accounts'],
            module_params['write_mode'],
            module_params['ai_type']
        )
