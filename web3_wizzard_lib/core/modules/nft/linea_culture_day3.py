from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.linea_day_3_contract import LineaDay3
from web3_wizzard_lib.core.utils.sub_module import SubModule


class LineaCultureDay3(SubModule):
    module_name = 'LINEA_CULTURE_3'

    def execute(self, account: AppAccount, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        linea = LineaDay3('0x3685102bc3D0dd23A88eF8fc084a8235bE929f1c', web3)
        linea.claim(account)

    def log(self):
        return "LINEA CULTURE 3"
