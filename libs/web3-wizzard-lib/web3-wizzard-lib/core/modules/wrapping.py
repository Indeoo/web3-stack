from loguru import logger
from sybil_engine.contract.weth import WETH
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.balance import NotEnoughNativeBalance
from sybil_engine.domain.balance.balance_utils import interval_to_eth_balance, verify_balance, interval_to_weth_balance
from sybil_engine.module.module import Module
from sybil_engine.utils.utils import ConfigurationException
from sybil_engine.utils.validation_utils import validate_amount_interval
from sybil_engine.utils.web3_utils import init_web3


class Wrapping(Module):
    module_name = 'WRAPPING'
    module_config = 'wrap_config'
    allowed_chains = ['ZKSYNC', 'LINEA', 'BASE', 'SCROLL', 'ARBITRUM']
    sleep_after_var = True

    def execute(self, wrapping_chain, swap_amount_interval, action, account):
        self.sleep_after_var = True
        chain_instance = get_chain_instance(wrapping_chain)
        web3 = init_web3(chain_instance, account.proxy)

        weth_contract = get_tokens_for_chain(chain_instance['chain'])['WETH']
        weth = WETH(weth_contract, web3)

        if action == 'WRAP':
            amount_to_wrap = interval_to_eth_balance(swap_amount_interval, account, chain_instance['chain'], web3)

            logger.info(f"{action} {str(amount_to_wrap)}")

            native_balance = verify_balance(self.min_native_balance, chain_instance, account, web3)

            if swap_amount_interval == 'all_balance':
                amount_to_wrap = amount_to_wrap.minus(self.min_native_balance)

            if amount_to_wrap.wei > native_balance.wei:
                raise NotEnoughNativeBalance(
                    f"Account balance {native_balance} < {amount_to_wrap} amount to wrap.")

            weth.deposit(account, amount_to_wrap)
        elif action == 'UNWRAP':
            if swap_amount_interval == '':
                swap_amount_interval = 'all_balance'

            amount_to_unwrap = interval_to_weth_balance(
                swap_amount_interval,
                account,
                chain_instance['chain'],
                web3
            )

            if amount_to_unwrap.wei < 1000:
                logger.info(f"WETH balance is {amount_to_unwrap}, skip unwrapping")
                self.sleep_after_var = False
                return

            logger.info(f"{action} {amount_to_unwrap}")

            weth.withdraw(account, amount_to_unwrap)
        else:
            raise ConfigurationException(f'Wrong Action {action}')

    def parse_params(self, module_params):
        self.validate_supported_chain(module_params['chain'])
        validate_amount_interval(module_params['amount_interval'])

        return module_params['chain'], module_params['amount_interval'], module_params['action']

    def log(self):
        return "WRAPPING"

    def sleep_after(self):
        return self.sleep_after_var
