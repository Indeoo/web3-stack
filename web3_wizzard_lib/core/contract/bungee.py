from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/bungee.json")

bungee_chain_ids = {
    "BSC": 56,
    "OPTIMISM": 10,
    "POLYGON": 137,
    "BASE": 8453,
    "ARBITRUM": 42161,
    "AVALANCHE": 43114,
    "ZK_EVM": 1101,
    "ZKSYNC": 324
}


class Bungee(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def refuel(self, account, to_chain, amount):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)
        txn_params['value'] = amount

        return self.contract.functions.depositNativeToken(
            bungee_chain_ids[to_chain],
            sender
        ).build_transaction(txn_params)
