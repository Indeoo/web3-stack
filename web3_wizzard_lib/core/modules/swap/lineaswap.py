from sybil_engine.domain.dex import Dex

from web3_wizzard_lib.core.contract.lineaswaprouter import LineaSwapRouter


class LineaSwap(Dex):
    dex_name = 'lineaswap'
    swap_contract = "LINEASWAP"
    supported_chains = ['BASE', 'LINEA']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.linea_swap_router = LineaSwapRouter(self.chain_contracts[self.swap_contract], self.web3)
        self.weth_address = self.tokens['WETH']

    def swap_native_for_token(self, account, amount_to_swap, slippage, to_token_address):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, self.weth_address, to_token_address) * slippage)
        args = [account, amount_to_swap, self.weth_address, to_token_address, amount_out_min]
        func = self.linea_swap_router.swap_exact_eth_for_tokens

        return args, func

    def swap_token_for_native(self, account, amount_to_swap, from_token_address, slippage):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, from_token_address, self.weth_address) * slippage)
        args = [account, amount_to_swap, from_token_address, self.weth_address, amount_out_min]
        func = self.linea_swap_router.swap_exact_tokens_for_eth

        return args, func

    def swap_token_for_token(self, account, amount_to_swap, slippage, from_token_address, to_token_address):
        raise Exception("Not supported")

    def get_amount_out_min(self, amount_to_swap, from_token_address, to_token_address):
        return self.linea_swap_router.get_amount_out(amount_to_swap, from_token_address, to_token_address)
