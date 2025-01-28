import random

from loguru import logger
from sybil_engine.config.app_config import get_cex_data, get_cex_conf
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance_utils import get_native_balance, \
    interval_to_native_balance, interval_to_erc20_balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.domain.cex.binance import Binance
from sybil_engine.domain.cex.okx import OKX
from sybil_engine.module.module import Module
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.utils import randomized_sleeping, ConfigurationException
from sybil_engine.utils.web3_utils import init_web3


class CEXWithdraw(Module):
    module_name = 'CEX_WITHDRAW'
    sleep_after_conf = True
    module_config = 'cex_withdraw'

    def execute(self, chain, withdraw_interval, min_auto_withdraw_interval, token, cex, account: AppAccount):
        self.sleep_after_conf = True
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, None)

        balance, min_auto_withdraw, withdraw_token = self.balance(account, chain, chain_instance,
                                                                  min_auto_withdraw_interval, token, web3)
        logger.info(f"{chain}")
        logger.info(f"Minimum balance should be {min_auto_withdraw}")

        if min_auto_withdraw.wei < balance.wei:
            self.sleep_after_conf = False

        while min_auto_withdraw.wei > balance.wei:
            logger.info(f"Actual balance: {balance}")

            amount = round(random.uniform(withdraw_interval['from'], withdraw_interval['to']), 6)
            logger.info(f"Withdraw {amount} {chain_instance['gas_token']} from {cex} to {account.address}")

            password, cex_data = get_cex_data()

            if cex == 'okx':
                cex_obj = OKX(cex_data[get_cex_conf()], password)
            elif cex == 'binance':
                cex_obj = Binance(cex_data[get_cex_conf()], password)
            else:
                raise ConfigurationException(f"{cex} is not")

            if withdraw_token == 'WETH':
                withdraw_token = 'ETH'

            cex_obj.withdrawal(account.address, chain, amount, withdraw_token)

            randomized_sleeping({'from': 60 * 2, 'to': 60 * 4})

            balance, _, _ = self.balance(account, chain, chain_instance, min_auto_withdraw_interval, token, web3)

    def balance(self, account, chain, chain_instance, min_auto_withdraw_interval, token, web3):
        if token == 'NATIVE':
            min_auto_withdraw = interval_to_native_balance(min_auto_withdraw_interval, account, chain, web3)
            balance = get_native_balance(account, web3, chain_instance)
            withdraw_token = chain_instance['gas_token']
        elif token in ['USDC', 'USDT', 'WETH', 'ETH']:
            if token == 'ETH':
                token = 'WETH'
            min_auto_withdraw = interval_to_erc20_balance(min_auto_withdraw_interval, account, token, chain, web3)
            erc20_token = Erc20Token(chain, token, web3)
            balance = erc20_token.balance(account)
            withdraw_token = token
        else:
            raise ConfigurationException(f"Unsupported token {token}, supported tokens are: NATIVE, USDC")
        return balance, min_auto_withdraw, withdraw_token

    def log(self):
        return "CEX WITHDRAW"

    def parse_params(self, module_params):
        if 'cex' not in module_params:
            module_params['cex'] = 'okx'

        return [
            module_params['chain'],
            module_params['withdraw_interval'],
            module_params['min_auto_withdraw_interval'],
            module_params['token'],
            module_params['cex']
        ]

    def sleep_after(self):
        return self.sleep_after_conf
