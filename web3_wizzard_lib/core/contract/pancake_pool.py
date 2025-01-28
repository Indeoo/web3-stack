from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/pancake/factory.json")


class PancakePool(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def get_pool(self, from_token: str, to_token: str):

        pool = self.contract.functions.getPool(
            from_token,
            to_token,
            500
        ).call()

        return pool
