from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/mendi_token.json")


class MendiTokenContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def mint(self, account, amount):
        txn_params = self.build_generic_data(account.address, False)

        return self.contract.functions.mint(amount).build_transaction(txn_params)

    @evm_transaction
    def redeem(self, account, amount):
        txn_params = self.build_generic_data(account.address, False)

        return self.contract.functions.redeemUnderlying(amount).build_transaction(txn_params)

    def balance_of(self, account):
        return self.contract.functions.balanceOfUnderlying(account.address).call()
