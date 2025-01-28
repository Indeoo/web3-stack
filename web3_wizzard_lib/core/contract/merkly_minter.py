from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction, l0_evm_transaction
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/merkly.json")


class MerklyMinter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def mint(self, account):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = Web3.to_wei(0.0004, "ether")
        contract_txn = self.contract.functions.mint().build_transaction(txn_params)

        return contract_txn

    @l0_evm_transaction
    def refuel(self, account, to_chain_id, amount_wei, fee):
        txn_params = self.build_generic_data(account.address, False)

        hex_amount = self.decimal_to_hex_padded(amount_wei)

        txn_params['value'] = amount_wei + fee
        contract_txn = self.contract.functions.bridgeGas(
            to_chain_id,
            account.address,
            f'0x00020000000000000000000000000000000000000000000000000000000000030d4000000000000000000000000000000000{hex_amount}{account.address[2:]}'
        ).build_transaction(txn_params)

        return contract_txn

    def estimate_send_fee(self, account, to_chain_id, hex_amount):
        return self.contract.functions.estimateSendFee(
            to_chain_id,
            b'0x',  # _zroPaymentAddress
            f'0x00020000000000000000000000000000000000000000000000000000000000030d4000000000000000000000000000000000{hex_amount}{account.address[2:]}'
            # _adapterParams
        ).call()[0]

    def decimal_to_hex_padded(self, decimal_number):
        hex_number = hex(decimal_number)[2:]  # Remove the '0x' prefix
        return hex_number.zfill(32)  # Pad with zeros to make the length 32
