import random

from sybil_engine.data.networks import get_chain_instance, get_ids_chain


class Contract:

    def __init__(self, contract_address, web3, abi=None):
        self.contract_address = contract_address
        self.web3 = web3
        self.chain_instance = get_chain_instance(get_ids_chain()[web3.eth.chain_id])
        if abi is not None:
            self.contract = web3.eth.contract(address=contract_address, abi=abi)

    def build_generic_data(self, sender, set_contract_address=True):
        txn_data = {
            "chainId": self.web3.eth.chain_id,
            'from': sender,
            'nonce': self.web3.eth.get_transaction_count(sender),
        }

        if not self.chain_instance['eip1599']:
            random_multiplier = random.uniform(1.1, 1.2)
            txn_data['gasPrice'] = int(self.web3.eth.gas_price * random_multiplier)

        if set_contract_address:
            txn_data['to'] = self.contract_address

        return txn_data
