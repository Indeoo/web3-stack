from sybil_engine.domain.dex import Dex

from web3_wizzard_lib.core.contract.horizondex_router import HorizonDexRouter
from ...contract.horizondex_quoter import HorizonDexQuoter


class Horizondex(Dex):
    dex_name = 'horizondex'
    swap_contract = 'HORIZONDEX'
    supported_chains = ['BASE', 'LINEA']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.weth_address = self.tokens['WETH']
        self.horizondex_router = HorizonDexRouter(self.chain_contracts[self.swap_contract], self.web3)

    def swap_token_for_native(self, account, amount_to_swap, from_token_address, slippage):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, from_token_address, self.weth_address) * slippage)
        args = [account, amount_to_swap, amount_out_min, from_token_address, self.weth_address]
        func = self.horizondex_router.multicall

        return args, func

    def swap_native_for_token(self, account, amount_to_swap, slippage, to_token_address):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, self.weth_address, to_token_address) * slippage)
        args = [account, amount_to_swap, amount_out_min, self.weth_address, to_token_address]
        func = self.horizondex_router.swap_exact_input_single

        return args, func

    def swap_token_for_token(self, account, amount_to_swap, slippage, from_token_address, to_token_address):
        raise Exception("Not supported yet")

    def get_amount_out_min(self, amount_to_swap, from_token_address, to_token_address):
        horizondex_quoter_contract = self.chain_contracts["HORIZONDEX_QUOTER"]
        horizondex_quoter = HorizonDexQuoter(horizondex_quoter_contract, self.web3)

        return horizondex_quoter.quote_exact_input_single(amount_to_swap.wei, from_token_address, to_token_address)
