from datetime import datetime

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/lineaswap_router.json")


class LineaSwapRouter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def swap_exact_eth_for_tokens(self, account, amount_to_swap, token_in_address, token_out_address, amount_out_min):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)
        txn_params['value'] = amount_to_swap.wei if amount_to_swap.token == 'ETH' else 10000000000000

        paths = [token_in_address, token_out_address]
        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)

        return self.contract.functions.swapExactETHForTokens(
            amount_out_min,
            paths,
            sender,
            deadline
        ).build_transaction(txn_params)

    @evm_transaction
    def swap_exact_tokens_for_eth(self, account, amount_to_swap, token_in_address, token_out_address, amount_out_min):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)

        paths = [token_in_address, token_out_address]
        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)

        return self.contract.functions.swapExactTokensForETH(
            amount_to_swap.wei,
            amount_out_min,
            paths,
            sender,
            deadline
        ).build_transaction(txn_params)

    def get_amount_out(self, amount_to_swap, token_in_address, token_out_address):
        return self.contract.functions.getAmountsOut(
            amount_to_swap.wei,
            [token_in_address, token_out_address]
        ).call()[1]
