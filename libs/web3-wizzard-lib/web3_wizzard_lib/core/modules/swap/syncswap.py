from sybil_engine.domain.dex import Dex

from web3_wizzard_lib.core.contract.syncswap_classic_pool_factory import SyncSwapClassicPoolFactory
from web3_wizzard_lib.core.contract.syncswap_pool import SyncSwapPoolContract
from web3_wizzard_lib.core.contract.syncswap_router import SyncSwapRouter


class Syncswap(Dex):
    dex_name = 'syncswap'
    swap_contract = 'SYNCSWAP'
    supported_chains = ['ZKSYNC', 'LINEA', 'SCROLL']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.weth_address = self.tokens['WETH']
        self.pool_classic_pool_factory_address = self.chain_contracts['SYNCSWAP_CLASSIC_POOL_FACTORY']
        self.syncswap_contract_address = self.chain_contracts[self.swap_contract]
        self.syncswap_router = SyncSwapRouter(self.syncswap_contract_address, self.web3)

    def swap_native_for_token(self, account, amount_to_swap, slippage, to_token_address):
        token_in_data_address = self.weth_address
        token_in_address = self.tokens['ZERO_ADDRESS']

        amount_out_min = int(
            self.get_amount_out_min(account, amount_to_swap, token_in_data_address, to_token_address) * slippage
        )

        args = [
            account,
            amount_to_swap,
            self.weth_address,
            token_in_address,
            self.get_pool_address(token_in_data_address, to_token_address),
            amount_out_min
        ]

        return args, self.syncswap_router.swap

    def swap_token_for_native(self, account, amount_to_swap, from_token_address, slippage):
        token_in_data_address = self.tokens[amount_to_swap.token]
        token_in_address = self.tokens[amount_to_swap.token]

        amount_out_min = int(
            self.get_amount_out_min(account, amount_to_swap, token_in_data_address, self.weth_address) * slippage)

        args = [account, amount_to_swap, token_in_address, token_in_data_address, self.get_pool_address(token_in_data_address, self.weth_address), amount_out_min]

        return args, self.syncswap_router.swap

    def get_amount_out_min(self, account, amount_to_swap, token_in_data_address, to_token_address):
        pool_address = self.get_pool_address(token_in_data_address, to_token_address)

        if isinstance(pool_address, str):
            syncswap_pool = SyncSwapPoolContract(pool_address, self.web3)
        else:
            syncswap_pool = SyncSwapPoolContract(list(pool_address.items())[0][1], self.web3)

        return syncswap_pool.get_amount_out(account, amount_to_swap, token_in_data_address)

    def get_pool_address(self, token_in_data_address, to_token_address):
        pool_factory = SyncSwapClassicPoolFactory(self.pool_classic_pool_factory_address, self.web3)
        return pool_factory.get_pool(token_in_data_address, to_token_address)
