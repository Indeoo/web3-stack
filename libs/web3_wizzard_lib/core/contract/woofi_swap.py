from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/woofi.json")


class WoofiSwap(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def swap(self, account, amount_to_swap, token_in_address, token_out_address, amount_out_min):
        sender = account.address
        txn_params = self.build_generic_data(sender, False)

        txn_params['value'] = amount_to_swap.wei if amount_to_swap.token == 'ETH' else 0

        return self.contract.functions.swap(
            token_in_address,
            token_out_address,
            amount_to_swap.wei,
            amount_out_min,
            sender,
            sender
        ).build_transaction(txn_params)

    def query_swap(self, from_token, to_token, from_amount):
        return self.contract.functions.querySwap(from_token, to_token, from_amount.wei).call()
