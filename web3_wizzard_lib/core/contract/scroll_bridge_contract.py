from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/scroll_bridge.json")


class ScrollBridgeContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def withdraw(
            self,
            account,
            amount_wei
    ):
        txn_params = self.build_generic_data(account.address, False)
        txn_params['value'] = amount_wei

        return self.contract.functions.withdrawETH(
            amount_wei,
            0
        ).build_transaction(txn_params)
