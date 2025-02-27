import random

from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import interval_to_eth_balance, from_eth_to_wei, verify_balance
from sybil_engine.module.module import Order, RepeatableModule
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.utils import ConfigurationException, interval_to_round
from sybil_engine.utils.validation_utils import validate_amount_interval, validate_interval
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.basiliskcontract import BasiliskContract
from web3_wizzard_lib.core.contract.eralendcontract import EraLendContract
from web3_wizzard_lib.core.contract.reactor_fusion_contract import ReactorFusionContract
from web3_wizzard_lib.core.modules.bank.layerbank import LayerBank
from web3_wizzard_lib.core.modules.bank.aave import Aave


class Lending(RepeatableModule):
    module_name = 'LENDING'
    module_config = 'lending_config'
    random_order = Order.RANDOM

    @RepeatableModule.repeatable_log
    def execute(self, lending_apps, amount: float, action: str, withdraw_sleep_interval: dict, chain,
                account: AppAccount):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        lending_app_name = random.choice(lending_apps)
        lending_app = self.get_lending_app(lending_app_name, chain, web3)

        verify_balance(self.min_native_balance, chain_instance, account, web3)

        if action == 'DEPOSIT':
            self.deposit(account, amount, lending_app, lending_app_name, chain, web3)
        elif action == 'WITHDRAW':
            self.withdraw(account, amount, chain, lending_app, lending_app_name)
        elif action == 'WITHDRAW_ALL':
            for app_name, app in self.lending_apps_with_deposit(account, chain, web3):
                self.withdraw(account, amount, chain, app, app_name)
        else:
            raise ConfigurationException("Unsupported action")

    def deposit(self, account, amount, lending_app, lending_app_name, chain, web3):
        amount_balance = interval_to_eth_balance(amount, account, chain, web3)

        if amount == 'all_balance':
            amount_balance = amount_balance.minus(self.min_native_balance)

        logger.info(f"Make deposit on {lending_app_name} | {amount_balance}")

        lending_app.mint(account, amount_balance.wei)

    def withdraw(self, account, amount, chain, lending_app, lending_app_name):
        deposit_balance = NativeBalance(lending_app.get_deposit_amount(account), chain, 'ETH')

        if deposit_balance.wei < 1000000000000:
            raise EmptyDepositException(f"[{account.address}] Deposit balance is 0, skip")

        logger.info(f"Deposit balance: {deposit_balance}")

        if amount == 'all_balance':
            withdraw_wei = deposit_balance.wei
        else:
            balance = NativeBalance(from_eth_to_wei(interval_to_round(amount)), chain, 'ETH')
            amount_balance = NativeBalance(int(balance.wei // 10000) * 10000, chain, balance.token)
            withdraw_wei = amount_balance.wei

            if deposit_balance.wei < withdraw_wei:
                logger.info(
                    f"Deposit {deposit_balance} < withdraw amount {amount_balance}"
                    f", withdrawing all deposit")
                withdraw_wei = deposit_balance.wei

        logger.info(f"Withdraw from {lending_app_name} | {deposit_balance}")

        lending_app.redeem_underlying(account, withdraw_wei)

    def get_lending_app(self, lending_app, chain, web3):
        lending_apps = self.get_lending_apps(chain, web3)

        if lending_app not in lending_apps.keys():
            raise ConfigurationException(f"{lending_app} not supported in {chain}. Supported lending: {list(lending_apps.keys())} supported")

        return lending_apps[lending_app]

    def get_lending_apps(self, chain, web3):
        contracts = get_contracts_for_chain(chain)

        apps = {
            'BASILISK_LANDING': BasiliskContract,
            'REACTORFUSION_LANDING': ReactorFusionContract,
            'ERALEND': EraLendContract,
            'AAVE': Aave,
            'LAYERBANK': LayerBank
        }

        return {k: v(contracts[k], web3) for k, v in apps.items() if k in contracts}

    def lending_apps_with_deposit(self, account, chain, web3):
        with_deposit = []

        for lending_app_name, lending_app in self.get_lending_apps(chain, web3).items():
            if lending_app.get_deposit_amount(account) > 1000000000000:
                with_deposit.append((lending_app_name, lending_app))

        return with_deposit

    def log(self):
        return "LENDING"

    def parse_params(self, module_params):
        validate_amount_interval(module_params['amount'])
        validate_interval(module_params['withdraw_sleep_interval'])

        if 'chain' not in module_params:
            module_params['chain'] = 'ZKSYNC'

        return [
            module_params['lending_apps'],
            module_params['amount'],
            module_params['action'],
            module_params['withdraw_sleep_interval'],
            module_params['chain']
        ]


class EmptyDepositException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
