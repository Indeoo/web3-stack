from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/yoddlo.json")


class YoddloContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def purchase(self, account):
        txn_params = self.build_generic_data(account.address, True)

        txn_params['value'] = 100000000000000
        txn_params['data'] = '0xfb89f3b1'

        return txn_params
