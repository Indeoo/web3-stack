from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/snap.json")


class SnapContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def stake(self, account, token_id):
        txn_params = self.build_generic_data(account.address, False)

        return self.contract.functions.stake(token_id).build_transaction(txn_params)