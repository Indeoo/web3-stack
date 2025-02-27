from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/new_rage_abi.json")


class NewRageContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def redeem(self, account, shares):
        txn_params = self.build_generic_data(account.address, False)

        contract_txn = self.contract.functions.redeem(
            shares,
            account.address,
            account.address,
        ).build_transaction(txn_params)

        return contract_txn

    def balance_of(self, account):
        return self.contract.functions.balanceOf(account.address).call()

    def convert_to_shares(self, amount):
        return self.contract.functions.convertToShares(amount).call()

    def max_redeem(self, account):
        return self.contract.functions.maxRedeem(account.address).call()
