from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.domain.dex import Dex

from web3_wizzard_lib.core.contract.maverick_multicall import MaverickMulticall
from ...contract.pancake_pool import PancakePool
from ...contract.pancake_quoter import PancakeQuoter

pool_addresses = {
    'ZKSYNC': {
        "ETH>USDC": "0x41c8cf74c27554a8972d3bf3d2bd4a14d8b604ab"
    },
    'BASE': {
        "ETH>USDbC": "0x06e6736ca9e922766279a22b75a600fe8b8473b6",
        "ETH>USDC": "0x06e6736ca9e922766279a22b75a600fe8b8473b6"
    }
}


class Maverick(Dex):
    dex_name = 'maverick'
    swap_contract = 'MAV_ROUTER'
    supported_chains = ['ZKSYNC', 'BASE']

    def __init__(self, chain_instance, web3):
        self.chain_instance = chain_instance
        super().__init__(chain_instance, web3)
        self.weth_contract = self.tokens['WETH']
        self.pancake_pool = PancakePool(self.chain_contracts["PANCAKE_FACTORY"], self.web3)
        self.maverick_router = MaverickMulticall(self.chain_contracts[self.swap_contract], self.web3)

    def swap_native_for_token(self, account, amount_to_swap, slippage, to_token_address):
        erc20_token = Erc20Token(self.chain_instance['chain'], to_token_address, self.web3)
        pair_name = f"{self.chain_instance['gas_token']}>{erc20_token.symbol()}"
        maverick_pool_address = pool_addresses[self.chain_instance['chain']][pair_name]

        pool = self.pancake_pool.get_pool(self.weth_contract, to_token_address)

        if pool == self.tokens['ZERO_ADDRESS']:
            raise Exception(f"[{account.address}] Swap path {self.weth_contract} to {to_token_address} not found!")

        amount_out = int(self.get_amount_out_min(amount_to_swap, self.weth_contract, to_token_address) * slippage)

        args = [account, amount_to_swap, amount_out, self.weth_contract, maverick_pool_address, to_token_address]

        return args, self.maverick_router.multicall

    def swap_token_for_native(self, account, amount_to_swap, from_token_address, slippage):
        pair_name = f'{self.chain_instance["gas_token"]}>{amount_to_swap.token}'
        maverick_pool_address = pool_addresses[self.chain_instance['chain']][pair_name]

        pool = self.pancake_pool.get_pool(from_token_address, self.weth_contract)

        if pool == self.tokens['ZERO_ADDRESS']:
            raise Exception(f"[{account.address}] Swap path {from_token_address} to {self.weth_contract} not found!")

        amount_out = int(self.get_amount_out_min(amount_to_swap, from_token_address, self.weth_contract) * slippage)

        args = [account, amount_to_swap, amount_out, from_token_address, maverick_pool_address, self.weth_contract]

        return args, self.maverick_router.multicall

    def get_amount_out_min(self, amount_to_swap, token_in_address, token_out_address):
        pancake_quoter_contract = self.chain_contracts["PANCAKE_QUOTER"]
        pancake_quoter = PancakeQuoter(pancake_quoter_contract, self.web3)

        return pancake_quoter.quote_exact_input_single(token_in_address, token_out_address, amount_to_swap.wei)
