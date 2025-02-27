from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.merkly_minter import MerklyMinter
from web3_wizzard_lib.core.utils.sub_module import SubModule


class MerklyMinterModule(SubModule):
    module_name = "MERKLY_MINTER"

    def execute(self, account, chain='ZKSYNC'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['MERKLY']
        merkly_minter = MerklyMinter(contract_address, web3)

        merkly_minter.mint(account)

    def log(self):
        return "MERKLY MINTER"
