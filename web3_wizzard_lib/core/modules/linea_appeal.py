import random
import webbrowser

from loguru import logger
from sybil_engine.module.module import Module
from sybil_engine.utils.accumulator import add_accumulator, get_value

from web3_wizzard_lib.core.utils.ai_utils import get_ai_chat

from web3_wizzard_lib.core.utils.module_memory import get_by_key, accumulate_by_key, remove_key, add_value
from web3_wizzard_lib.core.utils.statistic_utils import get_statistic_writer, statistic_date_string

APPEAL_ACCOUNTS = "APPEAL_ACCOUNTS"
APPEAL_ACCOUNTS_AMOUNT = "APPEAL_ACCOUNTS_AMOUNT"


class LineaAppeal(Module):
    module_name = 'LINEA_APPEAL'
    module_config = "linea_appeal_config"
    base_url = "https://docs.google.com/forms/d/e/1FAIpQLSfkbHzC1hZTy6u5R8S5i6wQ2xCyUZQjvucmlyChwg04fJIO5Q/viewform"

    def execute(self, token, accounts, statistic_write, ai_type, account):
        with open("resources/linea_appeal.txt") as f:
            self.linea_appeal_reason = f.read()

        with open("resources/ai_style_randomized.txt") as f:
            self.lines = f.readlines()

        with open("resources/ai_reason_randomized.txt") as f:
            self.reason_lines = f.readlines()

        add_accumulator("Acc Num", 1)

        statistics = get_statistic_writer()
        statistics.init_if_required(
            f"linea_appeal_{statistic_date_string}",
            ["#", "MainAddress", "GPT Answer"]
        )

        chat_gpt = get_ai_chat(ai_type, token)

        if get_by_key(APPEAL_ACCOUNTS_AMOUNT) is None:
            add_value(
                APPEAL_ACCOUNTS_AMOUNT,
                random.randint(accounts['from'], accounts['to'])
            )

        accumulate_by_key(
            APPEAL_ACCOUNTS, {
                "address": account.address,
            }
        )

        logger.info(f"Acc: {get_value("Acc Num")}")
        logger.info(f"Acc Amount: {get_value("Acc Amount")}")

        if (get_by_key(APPEAL_ACCOUNTS_AMOUNT) == len(get_by_key(APPEAL_ACCOUNTS))
                or get_value("Acc Num") == get_value("Acc Amount")):
            ai_style_randomized = random.choice(self.lines)
            selected_lines = random.sample(self.reason_lines, k=random.choice([2, 3]))

            reason = chat_gpt.ask(
                self.linea_appeal_reason
                    .replace("{random_style}", ai_style_randomized)
                    .replace("{random_reasons}", str(selected_lines))
            )
            logger.info(reason)

            statistics.write_row(
                statistic_date_string,
                [account.app_id, account.address, reason]
            )

            wallets = get_by_key(APPEAL_ACCOUNTS)
            address_list = [wallet["address"] for wallet in wallets]
            address_list.remove(account.address)
            self.open_appeal_form(account, "\n".join(address_list), reason)
            remove_key(APPEAL_ACCOUNTS)
            remove_key(APPEAL_ACCOUNTS_AMOUNT)

    def open_appeal_form(self, account, address_list, formatted_string):
        payload = {
            "entry.1292139045": account.address,
            "entry.1099559693": address_list.replace("\n", "%0A"),
            "entry.1296389817": formatted_string.replace("\n", "%0A")
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
