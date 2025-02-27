from datetime import datetime

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.data.networks import get_ids_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/velocore.json")


class VelocoreRouter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def swap_exact_eth_for_tokens(self, account, amount_to_swap, token_in_address, token_out_address, amount_out_min):
        sender = account.address

        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)
        stable = False

        txn_params = self.build_generic_data(sender)

        txn_params['value'] = amount_to_swap.wei
        txn_params['data'] = self.contract.encode_abi('swapExactETHForTokens', args=(
            amount_out_min,
            [[token_in_address, token_out_address, stable]],
            sender,
            deadline
        )
                                                     )

        return txn_params

    @evm_transaction
    def swap_exact_tokens_for_eth(self, account, amount_to_swap, token_in_address, token_out_address, amount_out_min):
        sender = account.address
        txn_params = self.build_generic_data(account.address, False)

        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)
        stable = False

        return self.contract.functions.swapExactTokensForETH(
            amount_to_swap.wei,
            amount_out_min,
            [[token_in_address, token_out_address, stable]],
            sender,
            deadline
        ).build_transaction(txn_params)

    @evm_transaction
    def swap_exact_tokens_for_tokens(self, account, amount_to_swap, token_in_address, token_out_address,
                                     amount_out_min):
        sender = account.address
        txn_params = self.build_generic_data(sender)

        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)

        usdc_address = get_tokens_for_chain(get_ids_chain()[self.web3.eth.chain_id])['USDC']

        if token_out_address != usdc_address:
            stable = False
        else:
            stable = True

        return self.contract.functions.swapExactTokensForTokens(
            amount_to_swap.wei,
            amount_out_min,
            [[token_in_address, token_out_address, stable]],
            sender,
            deadline
        ).build_transaction(txn_params)

    def get_amount_out(self, amount_to_swap, token_in_address, token_out_address):
        return self.contract.functions.getAmountOut(
            amount_to_swap.wei,
            token_in_address,
            token_out_address
        ).call()[0]
