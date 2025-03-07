from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance_utils import get_native_balance, interval_to_eth_balance, \
    interval_to_erc20_balance
from sybil_engine.module.module import Order, Module
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.retry import retry
from sybil_engine.utils.utils import ConfigurationException
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.bank.basilisk import Basilisk
from web3_wizzard_lib.core.modules.bank.cog_bank import Cog
from web3_wizzard_lib.core.modules.bank.compound_v3 import CompoundV3
from web3_wizzard_lib.core.modules.bank.eralend import Eralend
from web3_wizzard_lib.core.modules.bank.layerbank import LayerBank
from web3_wizzard_lib.core.modules.bank.mendi_finance import MendiFinance
from web3_wizzard_lib.core.modules.bank.aave import Aave
from web3_wizzard_lib.core.modules.bank.reactorfusion import ReactorFusion
from web3_wizzard_lib.core.modules.bank.zerolend import ZeroLend


class Banking(Module):
    module_name = 'BANKING'
    random_order = Order.RANDOM
    module_config = 'banking_config'

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def execute(self, bank_app_name, action, token, amount_interval, chain, account: AppAccount):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)
        balance = get_native_balance(account, web3, chain_instance)

        logger.info(f"Balance {balance}")

        if token == 'ETH':
            amount = interval_to_eth_balance(amount_interval, account, chain, web3)
        else:
            amount = interval_to_erc20_balance(amount_interval, account, token, chain, web3)

        bank_app = self.get_bank_app(bank_app_name, chain, web3)

        logger.info(f"{bank_app.app_name} | {action}")

        self.perform_action(bank_app, action, amount, token, account)

    def perform_action(self, bank_app, action, amount, token, account):
        if action == 'SUPPLY':
            bank_app.supply(account, amount)
        elif action == 'BORROW':
            bank_app.borrow(account, amount)
        elif action == 'REPAY':
            amount = bank_app.get_repay_borrow_amount(account)

            if amount > 0:
                logger.info(f"Repay {amount} {token} in {bank_app.app_name}")
                bank_app.repay_borrow(account, amount)
            else:
                logger.info(f"{token} borrow balance is 0")
        elif action == 'REDEEM':
            amount = bank_app.get_deposit_amount(account, token)

            if amount > 0:
                logger.info(f"Redeem {amount} of {token} from {bank_app.app_name}")
                bank_app.redeem(account, amount, token)
            else:
                logger.info(f"{token} balance is 0")
        else:
            raise ConfigurationException("Unsupported action")

    def get_bank_app(self, bank_app, chain, web3):
        bank_app = self.get_bank_app_by_name(bank_app)

        if chain not in bank_app.supported_chains:
            raise ConfigurationException(
                f"{bank_app} not supported in {chain}. Supported chains: {bank_app.supported_chains}")

        return bank_app(chain, web3)

    def get_bank_app_by_name(self, bank_app_name):
        for bank_app in self.get_bank_apps():
            if bank_app.app_name == bank_app_name:
                return bank_app
        raise ConfigurationException(f"No Bank App with name {bank_app_name} found")

    def get_bank_apps(self):
        return {
            Basilisk,
            ReactorFusion,
            Eralend,
            MendiFinance,
            LayerBank,
            Aave,
            ZeroLend,
            CompoundV3,
            Cog
        }

    def log(self):
        return "BANKING"

    def parse_params(self, module_params):
        if 'chain' not in module_params:
            module_params['chain'] = 'LINEA'

        return [
            module_params['bank'],
            module_params['action'],
            module_params['token'],
            module_params['amount_interval'],
            module_params['chain']
        ]
