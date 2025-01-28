from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/tavaera_id.json")


class TavaeraID(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def mint_citizen_id(self, account):
        txn_params = self.build_generic_data(account.address, False)
        txn_params['value'] = Web3.to_wei(0.0003, "ether")

        contract_txn = self.contract.functions.mintCitizenId().build_transaction(txn_params)

        return contract_txn
