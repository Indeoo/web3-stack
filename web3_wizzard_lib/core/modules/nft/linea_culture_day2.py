from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.linea_day_2_contract import LineaDay2
from web3_wizzard_lib.core.utils.sub_module import SubModule


class LineaCultureDay2(SubModule):
    module_name = 'LINEA_CULTURE_2'

    def execute(self, account: AppAccount, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        linea = LineaDay2('0xB8DD4f5Aa8AD3fEADc50F9d670644c02a07c9374', web3)
        linea.approve(account)

    def log(self):
        return "LINEA CULTURE 2"
