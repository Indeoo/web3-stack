from web3_wizzard_lib.core.sybil_engine.contract import Contract
from web3_wizzard_lib.core.sybil_engine.contract.transaction_executor import evm_transaction
from web3_wizzard_lib.core.sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/zerolend_liquidity.json")

class ZeroLendLiqContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def create_lock(self, account, amount):
        sender = account.address
        txn_params = self.build_generic_data(sender, False)

        return self.contract.functions.createLock(
            int(amount.wei * 0.99),
            31536000,
            True
        ).build_transaction(txn_params)
