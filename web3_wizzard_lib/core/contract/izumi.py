from datetime import datetime

import requests
from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

swap_method_id = 'ac9650d8'
abi = load_abi("resources/abi/izumi.json")


class IzumiRouter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def multicall(self, account, amount_to_swap, amount_out_min, token_in_address, token_out_address):
        txn_params = self.build_generic_data(account.address, set_contract_address=True)

        if amount_to_swap.token == 'ETH':
            txn_params['value'] = amount_to_swap.wei  # amount in for ETH

        amount_in = decimal_to_padded_hexadecimal(amount_to_swap.wei, 64)
        deadline_hex = decimal_to_padded_hexadecimal(int(datetime.now().timestamp() + 60 * 60 * 3), 64)
        amount_out_min_hex = decimal_to_padded_hexadecimal(amount_out_min, 64)
        token_in_address = token_in_address[2:].lower()
        token_out_address = token_out_address[2:].lower()

        sender_padded = pad_hex(account.address, 64).lower()

        if amount_to_swap.token == 'ETH':
            swap_method = f'0x{swap_method_id}00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000001a0000000000000000000000000000000000000000000000000000000000000012475ceafe6000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000a0{sender_padded}{amount_in}{amount_out_min_hex}{deadline_hex}000000000000000000000000000000000000000000000000000000000000002b{token_in_address}000bb8{token_out_address}00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
            refund_method = '412210e8a00000000000000000000000000000000000000000000000000000000'
            txn_params['data'] = swap_method + refund_method
        else:
            swap_method = f'0x{swap_method_id}00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000001a0000000000000000000000000000000000000000000000000000000000000012475ceafe6000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000{amount_in}{amount_out_min_hex}{deadline_hex}000000000000000000000000000000000000000000000000000000000000002b{token_in_address}000bb8{token_out_address}000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044'
            unwrap_method = f'49404b7c0000000000000000000000000000000000000000000000000000000000000000{sender_padded}00000000000000000000000000000000000000000000000000000000'
            txn_params['data'] = swap_method + unwrap_method

        return txn_params

    def quote_price(self, token):
        BASE_URL = 'https://api.izumi.finance/api/v1/token_info/price_info/?t=USDC&t=ETH&t=WETH&t=wstETH&t=weETH'
        response = requests.get(BASE_URL)

        if response.status_code == 200:
            data = response.json()
            tokenPrice, ETH = float(data['data'][token]), float(data['data']['ETH'])

            return ETH / tokenPrice
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None


def decimal_to_padded_hexadecimal(decimal_number, desired_length):
    hex_value = hex(decimal_number)[2:]

    return hex_value.zfill(desired_length)


def pad_hex(un_padded_hex, desired_length):
    return un_padded_hex[2:].zfill(desired_length)
