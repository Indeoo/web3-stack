from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction

from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/rage_claim.json")


class RageClaimer(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def claim(self, account, amount, index, merkle_proof):
        txn_params = self.build_generic_data(account.address, False)

        contract_txn = self.contract.functions.claim(
            index,
            account.address,
            amount,
            merkle_proof
        ).build_transaction(txn_params)

        return contract_txn
