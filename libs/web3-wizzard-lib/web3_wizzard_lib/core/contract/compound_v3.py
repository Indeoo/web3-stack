from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/compound_v3.json")


class CompoundV3Contract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def user_collateral(self, account, token_address):
        return self.contract.functions.userCollateral(
            account.address,
            token_address
        ).call()[0]
