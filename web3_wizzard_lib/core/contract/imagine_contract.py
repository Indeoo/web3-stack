from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/imagine.json")


class ImagineContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def mint(self, account, uri):
        amount = self.web3.to_wei(0.0001, "ether")
        txn_params = self.build_generic_data(account.address, set_contract_address=False)
        txn_params['value'] = amount

        return self.contract.functions.mint(uri).build_transaction(txn_params)
