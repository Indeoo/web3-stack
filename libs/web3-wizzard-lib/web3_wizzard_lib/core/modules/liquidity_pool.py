from venv import logger

from sybil_engine.data.networks import get_chain_instance
from sybil_engine.module.module import Module
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.validation_utils import validate_amount_interval
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.liquidity.syncswap_pool import SyncswapPool
from web3_wizzard_lib.core.modules.liquidity.velocore_pool import VelocorePool
from web3_wizzard_lib.core.modules.liquidity.nile_pool import NilePool
from web3_wizzard_lib.core.modules.liquidity.zerolend_liquidity import ZeroLendLiquidity


class LiquidityPool(Module):
    module_name = 'LIQUIDITY_POOL'
    module_config = 'liquidity_pool'

    def execute(self, action, amount_interval, token, dex, chain, account: AppAccount):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        if dex == 'syncswap':
            pool = SyncswapPool(chain_instance, web3)
        elif dex == 'velocore':
            pool = VelocorePool(chain_instance, web3)
        elif dex == 'nile':
            pool = NilePool(chain_instance, web3)
        elif dex == 'zerolend':
            pool = ZeroLendLiquidity(chain_instance, web3)
        else:
            raise Exception(f" {dex} Not supported")

        if action == 'DEPOSIT':
            logger.info(f"Deposit {token} to {dex}")
            pool.deposit(amount_interval, account, token, self.min_native_balance, chain)
        elif action == 'WITHDRAW':
            pool.withdraw(account, token, chain)
        else:
            raise Exception(f"{action} action not supported")

    def log(self):
        return "LIQUIDITY_POOL"

    def parse_params(self, module_params):
        validate_amount_interval(module_params['amount'])

        return [
            module_params['action'],
            module_params['amount'],
            module_params['token'],
            module_params['dex'],
            module_params['chain']
        ]


class EmptyDepositException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
