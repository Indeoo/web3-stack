from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/townstory_bonus.json")


class TownstoryBonusContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def claim_linea_travelbag(self, account, signature, deadline):
        txn_params = self.build_generic_data(account.address, False)

        return self.contract.functions.claimLineaTravelbag(
            signature, account.address, deadline
        ).build_transaction(txn_params)
