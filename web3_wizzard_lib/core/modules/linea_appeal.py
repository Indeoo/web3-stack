import webbrowser

from loguru import logger
from sybil_engine.module.module import Module
from sybil_engine.utils.statistic_utils import get_statistic_writer, statistic_date_string

from web3_wizzard_lib.core.utils.ai_utils import ChatGPT


class LineaAppeal(Module):
    module_name = 'LINEA_APPEAL'
    module_config = "linea_appeal_config"
    base_url = "https://docs.google.com/forms/d/e/1FAIpQLSfkbHzC1hZTy6u5R8S5i6wQ2xCyUZQjvucmlyChwg04fJIO5Q/viewform"

    with open("resources/linea_appeal.txt") as f:
        linea_appeal_reason = f.read()

    def execute(self, token, accounts, statistic_write, account):
        statistics = get_statistic_writer()
        statistics.init_if_required(
            statistic_date_string,
            ["#", "Address", "GPT Answer"]
        )

        chat_gpt = ChatGPT(token)

        reason = chat_gpt.ask(self.linea_appeal_reason)

        logger.info(reason)

        reason = reason['choices'][0]['message']['content']

        payload = {
            "entry.1292139045": account.address,
            "entry.1099559693": "",
            "entry.1296389817": reason
        }

        query_string = "&".join(f"{key}={value}" for key, value in payload.items())
        pre_filled_url = f"{self.base_url}?{query_string}"

        print(f"Opening form: {pre_filled_url}")

        statistics.write_row(
            statistic_date_string,
            [account.app_id, account.address, reason]
        )
        webbrowser.open(pre_filled_url)

    def parse_params(self, module_params):
        return module_params['token'], module_params['accounts'], module_params['write_mode']
