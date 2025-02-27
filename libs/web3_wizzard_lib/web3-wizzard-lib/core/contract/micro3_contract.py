from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/micro3.json")


class Micro3Contract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def purchase(self, account, amount):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = 80000000000000

        return self.contract.functions.purchase(amount).build_transaction(txn_params)
