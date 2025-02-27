from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/woofi.json")


class ZKDXContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)
        self.zkdx_token = '176211869ca2b568f2a7d4ee941e073a821ee1ff'

    @evm_transaction
    def swap_to_zkdx(self, account, amount):
        sender = account.address
        txn_params = self.build_generic_data(sender, True)

        amount_hex = self.decimal_to_hex_padded(amount.wei)
        txn_params[
            'data'] = f'0x045d0389000000000000000000000000{self.zkdx_token}00000000000000000000000000000000{amount_hex}'

        return txn_params

    @evm_transaction
    def swap_from_zkdx(self, account, amount):
        sender = account.address
        txn_params = self.build_generic_data(sender, True)

        amount_hex = self.decimal_to_hex_padded(amount)

        # txn_params['gas'] = 60000

        txn_params[
            'data'] = f'0x1e9a6950000000000000000000000000{self.zkdx_token}00000000000000000000000000000000{amount_hex}'

        return txn_params

    def decimal_to_hex_padded(self, decimal_number):
        hex_number = hex(decimal_number)[2:]  # Remove the '0x' prefix
        return hex_number.zfill(32)  # Pad with zeros to make the length 32
