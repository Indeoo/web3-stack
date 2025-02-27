from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/kreatorland.json")


class KreatorLandContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def mint(self, account, uri):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = 660000000000000
        contract_txn = self.contract.functions.mint(
            uri,
            1,
            660000000000000
        ).build_transaction(txn_params)

        return contract_txn
