from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.yuliverse_contract import YuliverseContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class Yuliverse(SubModule):
    module_name = 'YULIVERSE'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['YULIVERSE']
        yuliverse_nft = YuliverseContract(contract_address, web3)

        yuliverse_nft.purchase(account)

    def log(self):
        return "YULIVERSE NFT"
