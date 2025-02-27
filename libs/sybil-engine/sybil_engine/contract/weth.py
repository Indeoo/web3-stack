from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/weth.json")


class WETH(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def deposit(self, account, amount_to_swap):
        sender = account.address

        txn_params = self.build_generic_data(sender)
        txn_params['value'] = amount_to_swap.wei
        txn_params['data'] = self.contract.encode_abi("deposit")
        txn_params['gasPrice'] = self.web3.eth.gas_price

        return txn_params

    @evm_transaction
    def withdraw(self, account, amount_to_swap):
        sender = account.address

        txn_params = self.build_generic_data(sender)
        txn_params['data'] = self.contract.encode_abi("withdraw", args=(amount_to_swap.wei,))

        return txn_params

    def balance_of(self, account):
        return self.contract.functions.balanceOf(account.address).call()
