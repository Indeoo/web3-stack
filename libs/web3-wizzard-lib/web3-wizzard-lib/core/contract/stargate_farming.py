from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction

with open("resources/abi/stargate_farming.json") as f:
    abi = f.read()


class StargateFarming(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def deposit(self, account, pool_amount):
        sender = account.address
        txn_params = self.build_generic_data(sender, False)

        contract_txn = self.contract.functions.deposit(0, pool_amount.wei).build_transaction(txn_params)
        contract_txn['gas'] = int(self.web3.eth.estimate_gas(contract_txn) * 1.05)

        return contract_txn

    @evm_transaction
    def withdraw(self, account, amount_to_bridge):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)

        contract_txn = self.contract.functions.withdraw(
            0,
            amount_to_bridge
        ).build_transaction(txn_params)
        contract_txn['gas'] = int(self.web3.eth.estimate_gas(contract_txn) * 1.05)

        return contract_txn

    def user_info(self, account):
        return int(self.contract.functions.userInfo(0, account.address).call()[0])
