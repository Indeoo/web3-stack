from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.satoshi_universe_contract import SatoshiUniverseContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class SatoshiUniverse(SubModule):
    module_name = 'SATOSHI_UNIVERSE'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['SATOSHI_UNIVERSE']
        satoshi_universe = SatoshiUniverseContract(contract_address, web3)

        satoshi_universe.mint(account, 1)

    def log(self):
        return "SATOSHI UNIVERSE NFT"
