from sybil_engine.domain.dex import Dex

from web3_wizzard_lib.core.contract.velocore_router import VelocoreRouter


class Velocore(Dex):
    dex_name = 'velocore'
    swap_contract = "VELOCORE_ROUTER"
    supported_chains = ['ZKSYNC']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.weth_address = self.tokens['WETH']
        self.velocore_router = VelocoreRouter(self.chain_contracts[self.swap_contract], self.web3)

    def swap_native_for_token(self, account, amount_to_swap, slippage, to_token_address):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, self.weth_address, to_token_address) * slippage)

        args = [account, amount_to_swap, self.weth_address, to_token_address, amount_out_min]
        func = self.velocore_router.swap_exact_eth_for_tokens

        return args, func

    def get_amount_out_min(self, amount_to_swap, from_token_address, to_token_address):
        return self.velocore_router.get_amount_out(amount_to_swap, from_token_address, to_token_address)

    def swap_token_for_native(self, account, amount_to_swap, from_token_address, slippage):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, from_token_address, self.weth_address) * slippage)

        args = [account, amount_to_swap, from_token_address, self.weth_address, amount_out_min]
        func = self.velocore_router.swap_exact_tokens_for_eth
        return args, func

    def swap_token_for_token(self, account, amount_to_swap, slippage, from_token_address, to_token_address):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, from_token_address, to_token_address) * slippage)

        args = [account, amount_to_swap, from_token_address, to_token_address, amount_out_min]
        func = self.velocore_router.swap_exact_tokens_for_tokens

        return args, func
