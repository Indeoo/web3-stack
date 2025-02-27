import random

from web3 import Web3

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction


class DeployContract(Contract):

    @evm_transaction
    def deploy(self, account, data):
        sender = Web3.to_checksum_address(account.address)

        txn_params = self.build_generic_data(sender, False)
        txn_params['data'] = data
        txn_params['gasPrice'] = int(self.web3.eth.gas_price * random.uniform(1.1, 1.2))

        return txn_params
