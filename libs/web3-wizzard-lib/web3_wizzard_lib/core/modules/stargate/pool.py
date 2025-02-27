from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance_utils import get_native_balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.utils.utils import ModuleException
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.stargate_router import StargateRouter
from web3_wizzard_lib.core.contract.stargate_router_eth import StargateRouterEth
from web3_wizzard_lib.core.modules.stargate.stargate_balance_utils import StargatePoolToken


def add_to_pool(account, amount_to_pool, bridge_token, chain_instance, web3):
    def get_router_details(token_type, chain_inst):
        contracts = get_contracts_for_chain(chain_inst['chain'])
        if token_type == 'ETH':
            return StargateRouterEth(contracts["STARGATE_ROUTER_ETH"], web3), None
        else:
            erc20 = Erc20Token(chain_inst['chain'], token_type, web3)

            if erc20.allowance(account, contracts["STARGATE_ROUTER"]) < erc20.balance(account).wei:
                erc20.approve(account, contracts["STARGATE_ROUTER"])
            return StargateRouter(contracts["STARGATE_ROUTER"], web3), erc20

    logger.info(f"======= Adding liquidity {bridge_token} {chain_instance['chain']} ::: {account.address} =======")

    native_balance = get_native_balance(account, web3, chain_instance)
    logger.info(f"Native balance: {native_balance}")

    stargate_router, erc20 = get_router_details(bridge_token, chain_instance)

    balance = native_balance if bridge_token == 'ETH' else erc20.balance(account)
    if bridge_token != 'ETH':
        logger.info(f"Balance: {balance}")

    verify_balance(amount_to_pool, balance, native_balance)

    func = stargate_router.add_liquidity_eth if bridge_token == 'ETH' else stargate_router.add_liquidity

    logger.info(f"Pooling: {amount_to_pool}")
    func(account, amount_to_pool)


def verify_balance(amount_to_pool, balance, erc20_token):
    if amount_to_pool.wei > balance.wei:
        raise Exception(f"Account balance ({amount_to_pool}) is lower than amount to pool.")

    if balance.wei == 0:
        logger.info(f"{erc20_token.token} balance is 0")
        raise ModuleException("")


def find_max_pool_chain(balances):
    max_usdc_balance = max(balances, key=lambda x: x[1].wei)

    if max_usdc_balance[1] == 0:
        raise Exception("Can't bridge tokens, all chain USDC balances are zero")

    return max_usdc_balance


def get_pool_token_name(token_type):
    return 'STARGATE_ETH_POOL' if token_type == 'ETH' else 'STARGATE_USDT_POOL'


def get_pool_balances(token, account, chains):
    return [get_pool_balance_for_chain(chain, token, account) for chain in chains]


def get_pool_balance_for_chain(chain, pool_token_name, account):
    web3 = init_web3(get_chain_instance(chain), account.proxy)
    pool_token_instance = StargatePoolToken(chain, get_pool_token_name(pool_token_name), web3)
    return chain, pool_token_instance.balance(account), web3
