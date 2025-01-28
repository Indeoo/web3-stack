from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/empty_nft.json")


class EmptyNFT(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def mint(self, account):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)

        return self.contract.functions.mint().build_transaction(txn_params)
