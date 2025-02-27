import random

from web3 import Web3

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction


class Send(Contract):

    @evm_transaction
    def send_to_wallet(self, account, to_address, amount_to_swap, data=None):
        sender = Web3.to_checksum_address(account.address)

        txn_params = self.build_generic_data(sender, False)
        txn_params['value'] = amount_to_swap.wei
        txn_params['gasPrice'] = int(self.web3.eth.gas_price * random.uniform(1.1, 1.2))
        txn_params['to'] = Web3.to_checksum_address(to_address)

        if data is not None:
            txn_params['data'] = data

        return txn_params
