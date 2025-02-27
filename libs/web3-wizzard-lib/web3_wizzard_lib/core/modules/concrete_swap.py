import random

from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance_utils import verify_balance, amount_to_swap_from_interval
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.module.module import Module
from sybil_engine.utils.utils import SwapException
from sybil_engine.utils.validation_utils import validate_amount_interval, validate_token
from sybil_engine.utils.web3_utils import init_web3
from web3 import Web3

from web3_wizzard_lib.core.modules.swap.swap_list import swap_facade


class ConcreteSwap(Module):
    module_name = 'CONCRETE_SWAP'
    module_config = 'swap_config'
    allowed_chains = ['ZKSYNC', 'LINEA', 'BASE', 'SCROLL', 'ARBITRUM']
    sleep_after_var = True

    def execute(self, chain, amount_interval, from_token, to_token, swap_app, account):
        if isinstance(swap_app, list):
            swap_app = random.choice(swap_app)

        self.sleep_after_var = True
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        native_balance = verify_balance(self.min_native_balance, chain_instance, account, web3)

        from_token_contract = Erc20Token(chain, from_token, web3)
        to_token_contract = Erc20Token(chain, to_token, web3)

        if Web3.is_address(from_token):
            from_token_symbol = from_token_contract.symbol()
        else:
            from_token_symbol = from_token

        if Web3.is_address(to_token):
            to_token_symbol = to_token_contract.symbol()
        else:
            to_token_symbol = to_token

        pair_to_swap = self.create_pair_to_swap(
            from_token_symbol,
            swap_app,
            to_token_symbol,
        )

        amount_to_swap = amount_to_swap_from_interval(
            account,
            chain,
            self.min_native_balance,
            native_balance,
            amount_interval,
            from_token,
            web3
        )

        if amount_to_swap.wei < 100000:
            logger.info("Low balance, ignore")
            return

        try:
            swap_facade.swap(
                account,
                amount_to_swap,
                chain_instance,
                pair_to_swap,
                swap_app,
                from_token,
                to_token,
                web3
            )
        except SwapException as e:
            logger.info(e.message)
            self.sleep_after_var = False

    def create_pair_to_swap(self, from_token, swap_app, to_token):
        pair_to_swap = {
            'name': f'{from_token}>{to_token}',
            'tokens': [from_token, to_token],
            'slippage': 2,
            'app': swap_app
        }
        return pair_to_swap

    def log(self):
        return "SWAP"

    def sleep_after(self):
        return self.sleep_after_var

    def parse_params(self, module_params):
        self.validate_supported_chain(module_params['chain'])
        validate_amount_interval(module_params['amount_interval'])
        validate_token(module_params['from_token'])
        validate_token(module_params['to_token'])
        #validate_dex(module_params['app'])

        return (
            module_params['chain'],
            module_params['amount_interval'],
            module_params['from_token'],
            module_params['to_token'],
            module_params['app']
        )
