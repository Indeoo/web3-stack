from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.alienswap_contract import AlienSwapContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class AsMatch(SubModule):
    module_name = 'ASMATCH'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['ASMATCH']
        as_match_nft = AlienSwapContract(contract_address, web3)

        as_match_nft.purchase(account, 1)

    def log(self):
        return "ASMATCH NFT"
