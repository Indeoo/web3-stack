from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/zerolend.json")


class ZeroLendContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def deposit_eth(self, account, amount):
        sender = account.address
        txn_params = self.build_generic_data(sender, False)

        txn_params['value'] = amount

        return self.contract.functions.depositETH(
            '0x2f9bB73a8e98793e26Cb2F6C4ad037BDf1C6B269',
            account.address,
            0
        ).build_transaction(txn_params)

    @evm_transaction
    def withdraw_eth(self, account, amount):
        sender = account.address
        txn_params = self.build_generic_data(sender, False)

        return self.contract.functions.withdrawETH(
            '0x2f9bB73a8e98793e26Cb2F6C4ad037BDf1C6B269',
            int(amount * 0.98),
            account.address
        ).build_transaction(txn_params)
