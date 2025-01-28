from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/eth_scroll_bridge.json")


class EthScrollBridgeContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def sendMessage(self, account, amount, fee):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = amount + fee

        contract_txn = self.contract.functions.sendMessage(
            account.address,
            amount,
            b'0x',
            168000
        ).build_transaction(txn_params)

        return contract_txn
