from sybil_engine.data.contracts import get_contracts_for_chain


class Pool:
    pool_contract = ''

    def __init__(self, chain_instance, web3):
        self.chain_contracts = get_contracts_for_chain(chain_instance['chain'])
        self.velocore_pool_contract_address = self.chain_contracts[self.pool_contract]
        self.web3 = web3

    def deposit(self, amount_interval, account, token, min_native_balance, chain):
        pass

    def withdraw(self, account, token, chain):
        pass
