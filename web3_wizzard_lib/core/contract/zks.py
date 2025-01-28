from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/zks.json")


class ZKS(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def register(self, account, domain_name):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)

        contract_txn = self.contract.functions.register(domain_name, sender, 1).build_transaction(txn_params)
        contract_txn['gas'] = self.web3.eth.estimate_gas(contract_txn)

        return contract_txn

    def available(self, domain_name):
        return self.contract.functions.available(domain_name).call()
