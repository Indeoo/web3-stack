from loguru import logger

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi
from web3_wizzard_lib.core.contract.horizondex_router import decimal_to_padded_hexadecimal

abi = load_abi("resources/abi/compound_v3_bulker.json")


class CompoundV3BulkerContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def invoke(self, account, amount, actions):
        hex_amount = decimal_to_padded_hexadecimal(amount, 32)
        data = f'0x000000000000000000000000b2f97c1bd3bf02f5e74d13f02e3e26f93d77ce44000000000000000000000000ef0f48dadd0abe4f99b4c14862df303ba956bd1300000000000000000000000000000000{hex_amount}'

        txn = self.contract.functions.invoke(
            [hex_to_bytes(actions)],
            [hex_to_bytes(data)]
        )

        contract_txn = txn.build_transaction(self.build_generic_data(account.address, False))

        return contract_txn

def hex_to_bytes(hex_string):
    """
    Convert a hexadecimal string to bytes.

    Args:
        hex_string (str): The hexadecimal string, with or without '0x' prefix

    Returns:
        bytes: The converted bytes object
    """
    # Remove '0x' prefix if it exists
    if hex_string.startswith('0x'):
        hex_string = hex_string[2:]

    # Convert hex string to bytes
    return bytes.fromhex(hex_string)
