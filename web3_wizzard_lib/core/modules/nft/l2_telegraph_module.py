from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.l2_telegraph import L2TelegraphMinter
from web3_wizzard_lib.core.utils.sub_module import SubModule


class L2Telegraph(SubModule):
    module_name = "L2_TELEGRAPH_MINTER"

    def execute(self, account, chain='ZKSYNC'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['L2_TELEGRAPH']
        l2_telegraph = L2TelegraphMinter(contract_address, web3)

        l2_telegraph.mint(account)

    def log(self):
        return "L2 TELEGRAPH MINTER"
