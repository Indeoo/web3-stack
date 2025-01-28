from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.micro3_contract import Micro3Contract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class Micro3(SubModule):
    module_name = 'MICRO3'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['MICRO3']

        micro3_cotnract = Micro3Contract(contract_address, web3)

        micro3_cotnract.purchase(account, 1)

    def log(self):
        return "MICRO3 NFT"
