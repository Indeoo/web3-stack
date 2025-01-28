from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/abbysworld.json")


class ReadOnContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def curate(self, account, contentUrl):
        txn_params = self.build_generic_data(account.address, True)

        txn_params['data'] = f'0x7859bb8d{contentUrl}'
        txn_params['gasPrice'] = self.web3.eth.gas_price

        return txn_params
