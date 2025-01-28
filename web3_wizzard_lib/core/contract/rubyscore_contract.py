from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/rubyscore.json")


class RubyscoreContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def attest_rubyscore(self, account, signature, schemaId, expirationDate):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = 500000000000000

        signature_bytes = Web3.to_bytes(hexstr=signature[2:])

        contract_txn = self.contract.functions.attestRubyscore(
            (
                Web3.to_bytes(hexstr=schemaId[2:]),
                expirationDate,
                Web3.to_bytes(hexstr=f'000000000000000000000000{account.address[2:]}'),
                Web3.to_bytes(hexstr='0000000000000000000000000000000000000000000000000000000000000000'),
            ),
            [signature_bytes]  # Encapsulate in a list to match bytes[]
        ).build_transaction(txn_params)

        return contract_txn
