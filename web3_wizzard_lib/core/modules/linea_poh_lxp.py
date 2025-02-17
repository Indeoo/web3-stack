import requests
from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import Erc20Balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.module.module import Module
from sybil_engine.utils.accumulator import add_accumulator_balance, add_accumulator, get_value
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.utils.statistic_utils import statistic_date_string, get_statistic_writer


class LineaPOHLXP(Module):
    module_name = 'LINEA_POH_LXP'
    module_config = None

    lxp_contract = "0xd83af4fbD77f3AB65C3B1Dc4B38D7e67AEcf599A"

    def execute(self, account, chain="LINEA", statistic_write="GOOGLE"):
        poh = self.linea_poh_passed(account)

        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)
        erc20_token = Erc20Token(chain, self.lxp_contract, web3)
        balance = erc20_token.balance(account)

        logger.info(f"{account.address} balance is {balance}")
        job_name = f"lxp_{statistic_date_string}"
        statistics_writer = get_statistic_writer()

        statistics_writer.init_if_required(
            job_name,
            ['#', 'Address', 'rLXP', 'POH', 'LXP', 'Remark']
        )

        if poh:
            rLXP = balance
            add_accumulator_balance("Total rLXP", rLXP.wei)
        else:
            rLXP = Erc20Balance(0, 'LINEA', "LXP")

        add_accumulator_balance("Total LXP", balance.wei)
        add_accumulator("Acc Num", 1)

        row = [account.app_id, account.address, float(rLXP.readable()), poh, float(balance.readable()), ""]
        statistics_writer.write_row(job_name, row)

        if get_value("Acc Num") == get_value("Acc Amount"):
            row = [
                "TOTAL",
                "",
                float(get_value("Total rLXP").readable() / 10 ** 12),
                "",
                float(get_value("Total LXP").readable() / 10 ** 12),
                ""
            ]

            statistics_writer.write_row(job_name, row)

    def linea_poh_passed(self, account):
        result = requests.get(f"https://linea-xp-poh-api.linea.build/poh/{account.address}").json()
        return result["poh"]

    def log(self):
        return "LINEA POH LXP"
