from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi


abi = load_abi("resources/abi/tavaera.json")


class Tavaera(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def mint(self, account):
        txn_params = self.build_generic_data(account.address, False)

        contract_txn = self.contract.functions.mint().build_transaction(txn_params)

        return contract_txn
