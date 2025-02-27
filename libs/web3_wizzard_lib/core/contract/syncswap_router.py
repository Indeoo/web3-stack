from datetime import datetime

from eth_account.messages import encode_defunct
from sybil_engine.contract.contract import Contract
from sybil_engine.contract.erc20contract import MAX_ALLOWANCE
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/syncswap_router.json")


class SyncSwapRouter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def swap(self, account, amount_to_swap, token_in_data_address, token_in_address, pool_address, amount_out_min,
             withdraw_mode=b'\x01'):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)
        txn_params['value'] = amount_to_swap.wei if amount_to_swap.token == 'ETH' else 10000000000000

        steps = self.steps(amount_to_swap, pool_address, sender, token_in_address, token_in_data_address,
                           withdraw_mode)

        paths = [{"steps": steps, "tokenIn": token_in_address, "amountIn": amount_to_swap.wei}]
        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)

        return self.contract.functions.swap(paths, amount_out_min, deadline).build_transaction(txn_params)

    def steps(self, amount_to_swap, pool_address, sender, token_in_address, token_in_data_address, withdraw_mode):
        if isinstance(pool_address, str):
            data = b'\x00' * 12 + bytes.fromhex(token_in_data_address[2:]) + b'\x00' * 12 + bytes.fromhex(
                sender[2:]) + b'\x00' * 31 + withdraw_mode

            steps = [
                {
                    "pool": pool_address,
                    "data": data,
                    "callback": get_tokens_for_chain(amount_to_swap.chain)['ZERO_ADDRESS'],
                    "callbackData": b''
                }
            ]
        else:
            usdc_address = get_tokens_for_chain(amount_to_swap.chain)['USDC']

            pool_pairs = list(pool_address.items())
            if amount_to_swap.token == 'USDT':
                zero_pool = pool_pairs[0][1]  # USDC
                first_pool = pool_pairs[1][1]  # USDT

                data_fir_step = b'\x00' * 12 + bytes.fromhex(token_in_address[2:]) + b'\x00' * 12 + bytes.fromhex(
                    sender[2:]) + b'\x00' * 31 + b'\x00'

                data_sec_step = b'\x00' * 12 + bytes.fromhex(usdc_address[2:]) + b'\x00' * 12 + bytes.fromhex(
                    sender[2:]) + b'\x00' * 31 + withdraw_mode
            else:
                zero_pool = pool_pairs[1][1]  # USDT
                first_pool = pool_pairs[0][1]  # USDC

                data_fir_step = b'\x00' * 12 + bytes.fromhex(
                    token_in_data_address[2:]) + b'\x00' * 12 + bytes.fromhex(zero_pool[2:]) + b'\x00' * 31 + b'\x00'

                data_sec_step = b'\x00' * 12 + bytes.fromhex(usdc_address[2:]) + b'\x00' * 12 + bytes.fromhex(
                    sender[2:]) + b'\x00' * 31 + b'\x02'

            steps = [
                {
                    "pool": first_pool,
                    "data": data_fir_step,
                    "callback": get_tokens_for_chain(amount_to_swap.chain)['ZERO_ADDRESS'],
                    "callbackData": b''
                },
                {
                    "pool": zero_pool,
                    "data": data_sec_step,
                    "callback": get_tokens_for_chain(amount_to_swap.chain)['ZERO_ADDRESS'],
                    "callbackData": b''
                }
            ]

        return steps

    @evm_transaction
    def add_liquidity2(self, account, amount):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)

        txn_params['value'] = amount.wei

        return self.contract.functions.addLiquidity2(
            '0x814A23B053FD0f102AEEda0459215C2444799C70',
            [
                (
                    '0x0000000000000000000000000000000000000000',
                    amount.wei
                )
            ],
            f'0x000000000000000000000000{account.address[2:]}',
            0,
            '0x0000000000000000000000000000000000000000',
            b'0x'
        ).build_transaction(txn_params)

    @evm_transaction
    def burn_liquidity(self, account, pool, amount):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)

        return self.contract.functions.burnLiquiditySingle(
            pool,
            amount.wei,  # liqudity
            Web3.to_bytes(
                hexstr=f'0x0000000000000000000000005300000000000000000000000000000000000004000000000000000000000000{account.address[2:]}0000000000000000000000000000000000000000000000000000000000000001'),
            amount.wei,  # minAmount
            Web3.to_bytes(hexstr='0x0000000000000000000000000000000000000000'),
            b'0x'
        ).build_transaction(txn_params)
