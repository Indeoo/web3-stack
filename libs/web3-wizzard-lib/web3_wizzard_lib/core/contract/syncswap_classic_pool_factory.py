from web3_wizzard_lib.core.sybil_engine.contract import Contract
from web3_wizzard_lib.core.sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/syncswap_classic_pool_factory.json")


class SyncSwapClassicPoolFactory(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def get_pool(self, from_token, to_token):
        return self.contract.functions.getPool(
            from_token,
            to_token
        ).call()