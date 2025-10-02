import random

from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.data.pairs import Pairs
from sybil_engine.domain.balance.balance_utils import verify_balance, amount_to_swap_from_interval
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.module.module import Order, RepeatableModule
from sybil_engine.utils.utils import interval_to_int, randomized_sleeping, SwapException, ConfigurationException
from sybil_engine.utils.validation_utils import validate_amount_interval_possible_empty, validate_token, \
    validate_interval, validate_dex_list
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.swap.swap_list import swap_facade


class WarmUp(RepeatableModule):
    module_name = 'WARMUP'
    module_config = 'warmup_config'
    allowed_chains = ['ZKSYNC', 'LINEA', 'BASE', 'SCROLL', 'ARBITRUM']
    random_order = Order.RANDOM
    repeat_conf = 'amount_of_warmups'

    @RepeatableModule.repeatable_log
    def execute(self, chain, swap_amount_interval, warm_token, amount_of_warmups, allowed_dex, pair_names: list,
                sell_tokens, sleep_interval, account):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        swap_amount = interval_to_int(amount_of_warmups)

        if len(pair_names) > 0:
            logger.info(f"Warmup pairs {pair_names}")
        pair = Pairs(swap_facade)

        try:
            pair_swaps = pair.get_warmup_pair_swaps(allowed_dex, chain, pair_names, swap_amount, warm_token)
            random.shuffle(pair_swaps)
            pair, swaps = random.choice(pair_swaps)
        except ConfigurationException as e:
            pair_name = random.choice(pair_names)
            from_token = pair_name.split('>')[0]
            to_token = pair_name.split('>')[1]
            pair = self.create_pair_to_swap(from_token, allowed_dex, to_token)
            swaps = allowed_dex

        self._warm_up(chain_instance, pair, swaps, sell_tokens, sleep_interval, swap_amount_interval, account, web3)

    def _warm_up(self, chain_instance, pair, swaps, sell_tokens, sleep_interval, swap_amount_interval, account, web3):
        native_balance = verify_balance(self.min_native_balance, chain_instance, account, web3)
        buy_dex = random.choice(swaps)
        sell_dex = random.choice(swaps)

        self._warm_up_pair(buy_dex, sell_dex, native_balance, swap_amount_interval, chain_instance, pair, sell_tokens,
                           sleep_interval, account, web3)
        randomized_sleeping(sleep_interval)

    def _warm_up_pair(self, buy_dex, sell_dex, native_balance, swap_amount_interval, chain_instance, pair, sell_tokens,
                      sleep_interval, account, web3):
        from_token = pair['tokens'][0]
        to_token = pair['tokens'][1]

        amount_to_swap = amount_to_swap_from_interval(account, chain_instance['chain'], self.min_native_balance,
                                                      native_balance, swap_amount_interval, from_token, web3)
        swap_facade.swap(account, amount_to_swap, chain_instance, pair, buy_dex, from_token, to_token, web3)

        if sell_tokens:
            randomized_sleeping(sleep_interval)
            try:
                self.execute_sell(chain_instance, pair, sell_dex, account, web3)
            except SwapException as e:
                logger.error(e)
                self.execute_sell(chain_instance, pair, buy_dex, account, web3)

    def execute_sell(self, chain_instance, pair, sell_dex, account, web3):
        amount_to_swap = Erc20Token(chain_instance['chain'], pair['tokens'][1], web3).balance(account)
        swap_facade.swap(account, amount_to_swap, chain_instance, pair, sell_dex, amount_to_swap.token,
                         pair['tokens'][0], web3)

    def create_pair_to_swap(self, from_token, swap_app, to_token):
        pair_to_swap = {
            'name': f'{from_token}>{to_token}',
            'tokens': [from_token, to_token],
            'slippage': 2,
            'app': swap_app
        }
        return pair_to_swap

    def parse_params(self, module_params):
        self.validate_supported_chain(module_params['chain'])
        validate_amount_interval_possible_empty(module_params["swap_amount_interval"])
        validate_token(module_params["token"])
        validate_interval(module_params["amount_of_warmups"])
        validate_dex_list(module_params["allowed_dex"])
        validate_interval(module_params["pair_sleep_interval"])

        return (
            module_params["chain"],
            module_params["swap_amount_interval"],
            module_params["token"],
            module_params["amount_of_warmups"],
            module_params["allowed_dex"],
            module_params["warmup_pairs"],
            module_params["sell_tokens"],
            module_params["pair_sleep_interval"]
        )

    def log(self):
        return "WARM UP"

    def sleep_after(self):
        return False
