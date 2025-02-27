from sybil_engine.domain.dex import Dex

from web3_wizzard_lib.core.contract.pancake_quoter import PancakeQuoter
from web3_wizzard_lib.core.contract.pancake_router import PancakeRouter


class Pancake(Dex):
    dex_name = 'pancake'
    swap_contract = "PANCAKE_ROUTER"
    supported_chains = ['ZKSYNC', 'BASE', 'LINEA', 'ARBITRUM']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.weth_address = self.tokens['WETH']
        self.pancake_router_contract = self.chain_contracts[self.swap_contract]
        self.pancake_router = PancakeRouter(self.pancake_router_contract, self.web3)

    def swap_native_for_token(self, account, amount_to_swap, slippage, to_token_address):

        amount_out_min = int(self.get_amount_out_min(amount_to_swap, self.weth_address, to_token_address) * slippage)
        args = [account, amount_to_swap, self.weth_address, to_token_address, amount_out_min]
        func = self.pancake_router.swap_to_token

        return args, func

    def swap_token_for_native(self, account, amount_to_swap, from_token_address, slippage):
        amount_out_min = int(
            self.get_amount_out_min(amount_to_swap, from_token_address, self.weth_address) * slippage)

        args = [account, amount_to_swap, from_token_address, self.weth_address, amount_out_min]
        func = self.pancake_router.swap_to_eth
        return args, func

    def swap_token_for_token(self, account, amount_to_swap, slippage, from_token_address, to_token_address):
        raise Exception('Not supported')

    def get_amount_out_min(self, amount_to_swap, from_token_address, to_token_address):
        pancake_quoter_contract = self.chain_contracts["PANCAKE_QUOTER"]
        pancake_quoter = PancakeQuoter(pancake_quoter_contract, self.web3)

        return pancake_quoter.quote_exact_input_single(from_token_address, to_token_address, amount_to_swap.wei)
