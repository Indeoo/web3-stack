from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/satoshi_universe.json")


class SatoshiUniverseContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def mint(self, account, amount):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = 150000000000000

        contract_txn = self.contract.functions.mint(
            (
                account.address,
                '0xFf9B136F19D1Ad1f1716e2Ebe98b4A773f263275',
                amount,
                [],
                1,
                '0x'
            )
        ).build_transaction(txn_params)

        return contract_txn
