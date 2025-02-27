from loguru import logger
from sybil_engine.config.app_config import get_network
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import Erc20Balance, NativeBalance
from sybil_engine.domain.balance.balance_utils import get_native_balance, interval_to_eth_balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.module.module import Module
from sybil_engine.utils.utils import randomized_sleeping
from sybil_engine.utils.web3_utils import init_web3, get_amount_to_bridge_usdc, get_max_balance_data

from web3_wizzard_lib.core.contract.stargate_farming import StargateFarming
from web3_wizzard_lib.core.contract.stargate_router import StargateRouter
from web3_wizzard_lib.core.modules.stargate.pool import add_to_pool, find_max_pool_chain, get_pool_token_name, get_pool_balances
from web3_wizzard_lib.core.modules.stargate.stargate_balance_utils import StargatePoolToken

all_chains = {
    'MAIN': {
        'USDC': ['ARBITRUM', 'BASE', 'BSC', 'POLYGON', 'AVALANCHE', 'OPTIMISM', 'FANTOM'],
        'ETH': ['ARBITRUM', 'BASE', 'LINEA', 'OPTIMISM']
    },
    'LOCAL': {
        'USDC': ['BASE'],
        'ETH': ['BASE']
    },
    'GOERLI': {
        'USDC': ['LINEA', 'BASE'],
        'ETH': ['LINEA', 'BASE']
    }
}


class StargateFarmingModule(Module):
    module_name = 'STARGATE_FARMING'
    module_config = 'stargate_farming_config'

    def execute(self, bridge_amount_interval, chain, operation, all_balance_mode, token, operation_sleep_interval,
                account):
        try:
            logger.info(f"=============== Stargate staking: {account.address} ===============")

            chains = all_chains[get_network()][token]

            if 'ADD_TO_POOL' in operation:
                self.add_to_pool_logic(account, all_balance_mode, bridge_amount_interval, chain, chains, token)
                randomized_sleeping(operation_sleep_interval)

            if 'DEPOSIT' in operation:
                self.deposit_logic(account, chains, token)
                randomized_sleeping(operation_sleep_interval)

            if 'WITHDRAW' in operation:
                self.withdraw_logic(account, chains, token)
                randomized_sleeping(operation_sleep_interval)

            if 'REDEEM_FROM_POOL' in operation:
                self.redeem_from_pool_logic(account, chains, token)
                randomized_sleeping(operation_sleep_interval)
        except Exception as e:
            logger.info(f"Error during farming: {e}")

    def redeem_from_pool_logic(self, account, chains, token):
        pool_balances = get_pool_balances(token, account, chains)
        chain, pool_balance, web3 = find_max_pool_chain(pool_balances)
        chain_instance = get_chain_instance(chain)
        stargate_router = StargateRouter(get_contracts_for_chain(chain)["STARGATE_ROUTER"], web3)
        logger.info(f"Redeem from {chain} pool {pool_balance}")
        if token == 'USDC':
            stargate_pool_id = chain_instance['stargate_usdc_pool']
        else:
            stargate_pool_id = chain_instance['stargate_eth_pool']
        if pool_balance.wei > 0:
            stargate_router.instant_redeem(account, pool_balance.wei, stargate_pool_id)
        else:
            logger.info(f"Pool is empty, ignoring")

    def withdraw_logic(self, account, chains, token):
        logger.info("Withdraw from farming")
        farm_balances = self.get_farm_balances(account, token, chains)
        chain, farm_balance, web3 = find_max_pool_chain(farm_balances)
        farming_address = get_contracts_for_chain(chain)['STARGATE_FARMING']
        stargate_farming = StargateFarming(farming_address, web3)
        logger.info(f"Balance in farming {farm_balance}, withdrawing all")
        if farm_balance.wei > 0:
            stargate_farming.withdraw(account, farm_balance.wei)
        else:
            logger.info(f"Farming balance is empty, ignoring")

    def deposit_logic(self, account, chains, token):
        logger.info("Deposit to farm")

        pool_balances = get_pool_balances(token, account, chains)
        chain, pool_balance, web3 = find_max_pool_chain(pool_balances)

        chain_instance = get_chain_instance(chain)
        farming_address = get_contracts_for_chain(chain)['STARGATE_FARMING']

        stargate_farming = StargateFarming(farming_address, web3)
        logger.info(f"Amount in {chain} pool {pool_balance}")

        pool_token_name = get_pool_token_name(token)
        stargate_pool_token = StargatePoolToken(chain, pool_token_name, web3)

        if stargate_pool_token.allowance(account, farming_address) < pool_balance.wei:
            stargate_pool_token.approve(account, farming_address)

        stargate_farming.deposit(account, pool_balance)

    def add_to_pool_logic(self, account, all_balance_mode, bridge_amount_interval, chain, chains, token):

        def get_balance_to_pool(token_type, chain_instance, web3):
            if token_type == 'USDC':
                stargate_token = Erc20Token(chain, 'USDC', web3)
                return stargate_token.balance(account)
            else:
                return get_native_balance(account, web3, chain_instance)

        if bridge_amount_interval == 'all_balance':
            if all_balance_mode == 0:
                max_balance_chain, amount_to_pool, native_balance, web3 = get_max_balance_data(token, chains, account)
                chain_instance = get_chain_instance(max_balance_chain)
                amount_to_pool = native_balance
            else:
                chain_instance = get_chain_instance(chain)
                web3 = init_web3(chain_instance, account.proxy)
                amount_to_pool = get_balance_to_pool(token, chain_instance, web3)
            amount_to_pool = amount_to_pool.minus(self.min_native_balance)
        else:
            chain_instance = get_chain_instance(chain)
            web3 = init_web3(chain_instance, account.proxy)
            amount_to_pool = get_amount_to_bridge_usdc(
                bridge_amount_interval) if token == 'USDC' else interval_to_eth_balance(bridge_amount_interval, account,
                                                                                        chain_instance['chain'], web3)

        logger.info(f"Adding to stargate {chain_instance['chain']} pool")
        add_to_pool(account, amount_to_pool, token, chain_instance, web3)

    def get_farm_balances(self, account, token, chains):

        def get_balance_for_chain(chain):
            web3 = init_web3(get_chain_instance(chain), account.proxy)
            farming_address = get_contracts_for_chain(chain)['STARGATE_FARMING']
            farming = StargateFarming(farming_address, web3)

            if token == 'USDC':
                return chain, Erc20Balance(farming.user_info(account), chain, token), web3
            else:
                return chain, NativeBalance(farming.user_info(account), chain, token), web3

        return [get_balance_for_chain(chain) for chain in chains]

    def log(self):
        return "STARGATE FARMING"

    def parse_params(self, module_params):
        return (
            module_params['bridge_amount_interval'],
            module_params['chain'],
            module_params['operation'],
            module_params['all_balance_mode'],
            module_params['token'],
            module_params['operation_sleep_interval']
        )
