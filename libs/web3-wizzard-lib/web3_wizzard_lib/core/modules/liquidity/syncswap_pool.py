from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import interval_to_eth_balance
from sybil_engine.domain.balance.tokens import Erc20Token

from web3_wizzard_lib.core.contract.syncswap_pool import SyncSwapPoolContract
from web3_wizzard_lib.core.contract.syncswap_classic_pool import SyncSwapClassicPool
from web3_wizzard_lib.core.contract.syncswap_router import SyncSwapRouter
from web3_wizzard_lib.core.modules.liquidity.pool import Pool


class SyncswapPool(Pool):
    module_name = 'SYNCSWAP_LIQUIDITY'
    pool_contract = 'SYNCSWAP'

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.syncswap_router = SyncSwapRouter(self.velocore_pool_contract_address, self.web3)

    def deposit(self, amount_interval, account, token, min_native_balance, chain):
        amount = interval_to_eth_balance(amount_interval, account, chain, self.web3)

        pool = self.get_pool(chain)
        pool_amount = self.get_pool_amount(account, chain, pool)

        if pool_amount.wei < 10000000000:
            logger.info(f"Deposit {amount}")
            self.syncswap_router.add_liquidity2(account, amount)
        else:
            logger.info("This account already has deposit, skip")

    def withdraw(self, account, token, chain):
        pool = self.get_pool(chain)
        pool_amount = self.get_pool_amount(account, chain, pool)

        if pool_amount.wei < 10000000000:
            logger.info(f"Withdraw amount is to small")
            return

        erc20_token = Erc20Token(chain, pool, self.web3)

        if erc20_token.allowance(account, self.syncswap_router.contract_address) < pool_amount.wei:
            erc20_token.approve(account, self.syncswap_router.contract_address)

        print(erc20_token.balance(account).wei)

        logger.info(f"Withdraw {pool_amount}")
        self.syncswap_router.burn_liquidity(account, pool, pool_amount)

    def get_pool_amount(self, account, chain, pool):
        return NativeBalance(
            SyncSwapPoolContract(pool, self.web3).balanceOf(account),
            chain,
            'ETH'
        )

    def get_pool(self, chain):
        syncswap_classic_pool = SyncSwapClassicPool(get_contracts_for_chain(chain)["SYNCSWAP_CLASSIC_POOL_FACTORY"], self.web3)
        return syncswap_classic_pool.get_pool(get_tokens_for_chain(chain)['ETH'], get_tokens_for_chain(chain)['USDC'])
