from datetime import datetime

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

swap_method_id = 'a8c9ed67'
abi = load_abi("resources/abi/horizondex.json")


class HorizonDexRouter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def multicall(self, account, amount_to_swap, amount_out_min, token_in_address, token_out_address):
        txn_params = self.build_generic_data(account.address, set_contract_address=False)

        if amount_to_swap.token == 'ETH':
            txn_params['value'] = amount_to_swap.wei  # amount in for ETH

        deadline_hex = decimal_to_padded_hexadecimal(int(datetime.now().timestamp() + 60 * 60 * 3), 64)
        amount_in = decimal_to_padded_hexadecimal(amount_to_swap.wei, 64)
        amount_out_min_hex = decimal_to_padded_hexadecimal(amount_out_min, 64)
        token_in_address_padded = pad_hex(token_in_address, 64).lower()
        token_out_address_padded = pad_hex(token_out_address, 64).lower()

        if amount_to_swap.chain == 'BASE':
            some_value = '000000000000000000000000000000000000000000000000000000000000000a'
        else:
            if amount_to_swap.token == 'USDC':
                some_value = '000000000000000000000000000000000000000000000000000000000000012c'
            else:
                some_value = '0000000000000000000000000000000000000000000000000000000000000028'

        swap = '0x' + swap_method_id + token_in_address_padded + token_out_address_padded + some_value + '0000000000000000000000000000000000000000000000000000000000000000' + deadline_hex + amount_in + amount_out_min_hex + '0000000000000000000000000000000000000000000000000000000000000000'
        unwrapETH = self.contract.encode_abi("unwrapWeth", args=(amount_out_min, account.address))

        return self.contract.functions.multicall([swap, unwrapETH]).build_transaction(txn_params)

    @evm_transaction
    def swap_exact_input_single(self, account, amount_to_swap, min_amount_out, token_in_address, token_out_address):
        sender = account.address

        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)
        txn_params = self.build_generic_data(sender, set_contract_address=False)
        txn_params['value'] = amount_to_swap.wei

        return self.contract.functions.swapExactInputSingle(
            (
                token_in_address,
                token_out_address,
                40,
                sender,
                deadline,
                amount_to_swap.wei,
                min_amount_out,
                0
            ),
        ).build_transaction(txn_params)

    @evm_transaction
    def swap_exact_input(self, account, min_amount_out, amount_to_swap, token_in_address, token_out_address):
        sender = account.address

        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)
        path = token_in_address + '00002842000000000000000000000000000000000000060003e8' + token_out_address

        txn_params = self.build_generic_data(sender)
        txn_params['value'] = amount_to_swap.wei
        txn_params['data'] = self.contract.encode_abi('swapExactInput', args=(
            (
                path,
                sender,
                deadline,
                amount_to_swap.wei,
                min_amount_out
            ),
        )
                                                     )
        return txn_params


def decimal_to_padded_hexadecimal(decimal_number, desired_length):
    hex_value = hex(decimal_number)[2:]

    return hex_value.zfill(desired_length)


def pad_hex(un_padded_hex, desired_length):
    return un_padded_hex[2:].zfill(desired_length)
