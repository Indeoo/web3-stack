import time

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/omnisea.json")


class OmniSea(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def create(self, account, title, symbol):
        txn_params = self.build_generic_data(account.address, False)

        contract_txn = self.contract.functions.create([
            title,
            symbol,
            "",
            "",
            0,
            True,
            0,
            int(time.time()) + 1000000]
        ).build_transaction(txn_params)

        return contract_txn
