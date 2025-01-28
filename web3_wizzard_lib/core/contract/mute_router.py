from datetime import datetime

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.data.networks import get_ids_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/mute_router.json")


class MuteRouter(Contract):
    def __init__(self, contract_address, web3):
        tokens = get_tokens_for_chain(get_ids_chain()[web3.eth.chain_id])
        self.weth_address = tokens['WETH']
        self.usdc_address = tokens['USDC']
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def swap_exact_eth_for_tokens_supporting_fee_on_transfer_tokens(self, account, amount_to_swap, token_in_address,
                                                                    token_out_address, amount_out_min):
        sender = account.address

        path = [token_in_address, token_out_address]
        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)
        stable = [True, False] if token_out_address == self.usdc_address else [False, False]

        txn_params = self.build_generic_data(sender)

        txn_params['value'] = amount_to_swap.wei
        txn_params['data'] = self.contract.encode_abi('swapExactETHForTokensSupportingFeeOnTransferTokens', args=(
            amount_out_min,
            path,
            sender,
            deadline,
            stable
        )
                                                     )

        txn_params['gas'] = self.web3.eth.estimate_gas(txn_params)

        return txn_params

    @evm_transaction
    def swap_exact_tokens_for_eth_supporting_fee_on_transfer_tokens(self, account, amount_to_swap, token_in_address,
                                                                    token_out_address, amount_out_min):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)

        path = [token_in_address, token_out_address]
        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)
        stable = [False, False]

        contract_txn = self.contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amount_to_swap.wei,
            amount_out_min,
            path,
            sender,
            deadline,
            stable
        ).build_transaction(txn_params)

        return contract_txn

    @evm_transaction
    def swap_exact_tokens_for_tokens_supporting_fee_on_transfer_tokens(self, account, amount_to_swap, token_in_address,
                                                                       token_out_address, amount_out_min):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)

        path = [token_in_address, self.weth_address, token_out_address]
        deadline = int(datetime.now().timestamp() + 60 * 60 * 3)
        stable = [True, False, False] if token_in_address == self.usdc_address else [False, True, False]

        contract_txn = self.contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amount_to_swap.wei,
            amount_out_min,
            path,
            sender,
            deadline,
            stable
        ).build_transaction(txn_params)

        return contract_txn

    def get_amount_out(self, amount_to_swap, token_in_address, token_out_address):
        return self.contract.functions.getAmountOut(
            amount_to_swap.wei,
            token_in_address,
            token_out_address
        ).call()[0]
