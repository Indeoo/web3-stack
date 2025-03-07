from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/compound_v3.json")


class CompoundV3Contract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def borrow_balance_of(self, account):
        return self.contract.functions.borrowBalanceOf(account.address).call()

    @evm_transaction
    def supply(self, account, amount, token_address):
        txn_params = self.build_generic_data(account.address, set_contract_address=False)

        return self.contract.functions.supply(
            token_address,
            amount
        ).build_transaction(txn_params)

    def user_collateral(self, account, token_address):
        return self.contract.functions.userCollateral(
            account.address,
            token_address
        ).call()[0]
