from datetime import datetime

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.data.networks import get_ids_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.utils.file_loader import load_abi

swap_method_id = 'c04b8d59'

length_3c = '000000000000000000000000000000000000000000000000000000000000003c'
universal_value = '000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000a0'

abi = load_abi("resources/abi/maverick_multicall.json")


class MaverickMulticall(Contract):
    def __init__(self, contract_address, web3):
        self.weth_token = get_tokens_for_chain(get_ids_chain()[web3.eth.chain_id])['WETH']
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def multicall(self, account, amount_to_swap, amount_out_min_in, token_in_address, pool_address, token_out_address):
        txn_params = self.build_generic_data(account.address, False)

        if amount_to_swap.token == 'ETH':
            txn_params['value'] = amount_to_swap.wei  # amount in for ETH

        deadline_hex = decimal_to_padded_hexadecimal(int(datetime.now().timestamp() + 60 * 60 * 3), 64)
        amount_in = decimal_to_padded_hexadecimal(amount_to_swap.wei, 64)
        amount_out_min = decimal_to_padded_hexadecimal(amount_out_min_in, 64)
        recipient = pad_hex(account.address, 64) if token_out_address != self.weth_token else pad_hex('', 64)

        eth_to_usdc = '0x' + swap_method_id + universal_value + recipient + deadline_hex + amount_in + amount_out_min + length_3c + pad_hex(
            token_in_address, 40) + pad_hex(pool_address, 40) + pad_hex(token_out_address, 40) + '00000000'

        if token_out_address == self.weth_token:
            encoded_action = self.contract.encode_abi("unwrapWETH9", args=(amount_out_min_in, account.address))
        else:
            encoded_action = self.contract.encode_abi("refundETH") + pad_hex(account.address, 128)

        return self.contract.functions.multicall([eth_to_usdc, encoded_action]).build_transaction(txn_params)


def decimal_to_padded_hexadecimal(decimal_number, desired_length):
    hex_value = hex(decimal_number)[2:]

    return hex_value.zfill(desired_length)


def pad_hex(un_padded_hex, desired_length):
    return un_padded_hex[2:].zfill(desired_length)
