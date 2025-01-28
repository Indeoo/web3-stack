from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/era_ns.json")


class EraName(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def register(self, account, domain_name):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)
        txn_params['value'] = Web3.to_wei(0.003, "ether")

        return self.contract.functions.Register(domain_name).build_transaction(txn_params)

    def check_name(self, domain_name):
        return self.contract.functions._checkName(domain_name).call()
