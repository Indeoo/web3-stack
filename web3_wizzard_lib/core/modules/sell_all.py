import random

from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.data.pairs import Pairs
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.module.module import Module
from sybil_engine.utils.utils import randomized_sleeping
from sybil_engine.utils.validation_utils import validate_interval, validate_token
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.swap.swap_list import swap_facade


class SellAll(Module):
    module_name = 'SELL_ALL'
    module_config = 'sell_all_config'
    allowed_chains = ['ZKSYNC', 'LINEA', 'BASE', 'SCROLL', 'ARBITRUM']

    def execute(self, chain, sleep_interval, receive_token, account):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        pairs = Pairs(swap_facade)

        for pair, swaps in pairs.get_all_pair_swaps(chain, pairs.get_pair_names(chain, receive_token), receive_token):
            erc20_token = Erc20Token(chain, pair['tokens'][1], web3)

            amount_to_sell = erc20_token.balance(account)

            random_app = random.choice(swaps)

            logger.info(f"Sell all on {random_app}")

            if amount_to_sell.wei > 100:
                swap_facade.swap(account, amount_to_sell, chain_instance, pair, random_app, amount_to_sell.token,
                                 pair['tokens'][0], web3)
                randomized_sleeping(sleep_interval)

    def log(self):
        return "SELL ALL TOKENS"

    def parse_params(self, module_params):
        self.validate_supported_chain(module_params['chain'])
        validate_interval(module_params['sleep_interval'])
        validate_token(module_params['receive_token'])

        return module_params['chain'], module_params['sleep_interval'], module_params['receive_token']

    def sleep_after(self):
        return False
