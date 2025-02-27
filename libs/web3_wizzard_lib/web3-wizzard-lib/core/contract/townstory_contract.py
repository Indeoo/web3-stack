from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/townstory.json")


class TownstoryContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def create_account_sign(self, account, signature, deadline):
        txn_params = self.build_generic_data(account.address, False)

        contract_txn = self.contract.functions.createAccountSign(
            signature, 0, deadline
        ).build_transaction(txn_params)

        return contract_txn
