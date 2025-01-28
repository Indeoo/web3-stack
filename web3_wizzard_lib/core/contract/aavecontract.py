from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction

from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/aave.json")


class AaveContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def depositETH(self, account, amount: int):
        sender = account.address
        txn_params = self.build_generic_data(sender, set_contract_address=False)

        txn_params['value'] = amount

        return self.contract.functions.depositETH(
            '0x11fCfe756c05AD438e312a7fd934381537D3cFfe',
            account.address,
            0
        ).build_transaction(txn_params)

    @evm_transaction
    def withdrawETH(self, account, amount: int):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)

        return self.contract.functions.withdrawETH(
            '0x11fCfe756c05AD438e312a7fd934381537D3cFfe',
            amount,
            account.address
        ).build_transaction(txn_params)