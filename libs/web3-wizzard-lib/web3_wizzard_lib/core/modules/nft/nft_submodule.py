from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.utils.sub_module import SubModule


class NftSubmodule(SubModule):
    def execute(self, *args):
        pass

    def log(self):
        pass

    def create_web3(self, account, chain):
        chain_instance = get_chain_instance(chain)
        return init_web3(chain_instance, account.proxy)