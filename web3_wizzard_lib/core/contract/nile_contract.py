import random
from datetime import datetime

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/nile_pool.json")


class NileContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def add_liquidity_eth(self, account, token, max_token, amount_eth):
        tx_data = self.build_generic_data(account.address, False)

        deadline = int(datetime.now().timestamp()) + random.randint(60, 60 * 60 * 24)
        tx_data['value'] = amount_eth.wei

        return self.contract.functions.addLiquidityETH(
            token,
            False,
            int(max_token * 0.99),
            int(max_token * 0.95),
            int(amount_eth.wei * 0.95),
            account.address,
            deadline
        ).build_transaction(tx_data)

    @evm_transaction
    def remove_liquidity_eth(self, account, token, liquidity, amount_eth, max_token):
        tx_data = self.build_generic_data(
            account.address,
            False
        )

        deadline = int(datetime.now().timestamp()) + random.randint(60, 60 * 60 * 24)

        return self.contract.functions.removeLiquidityETH(
            token,
            False,
            int(liquidity * 0.99),
            int(max_token * 0.95),
            int(amount_eth * 0.95),
            account.address,
            deadline
        ).build_transaction(tx_data)

    def quote_remove_liquidity_eth(self, token_in, token_out, liquidity):
        return self.contract.functions.quoteRemoveLiquidity(token_in, token_out, False, liquidity).call()

    def get_amount_out(self, amount, from_token, to_token):
        return self.contract.functions.getAmountOut(
            amount.wei,
            Web3.to_checksum_address(from_token),
            Web3.to_checksum_address(to_token)
        ).call()
