from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/syncswap_classic_pool_factory.json")


class SyncSwapClassicPoolFactory(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def get_pool(self, from_token, to_token):
        return self.contract.functions.getPool(
            from_token,
            to_token
        ).call()