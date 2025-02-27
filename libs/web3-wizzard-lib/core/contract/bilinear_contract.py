from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/bilinear.json")


class BilinearContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def claim(self, account):
        txn_params = self.build_generic_data(account.address, False)

        return self.contract.functions.claim(
            [],
            ([], [1]),
            ([], [], []),
            0,
            '0x307b8d76e3a3ca16066982ae42768878ec07a1b9af2679f2f9b8a3c3db25e7d5'
        ).build_transaction(txn_params)
