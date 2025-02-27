from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.module.module import Order, Module
from sybil_engine.utils.accumulator import add_accumulator_balance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.dmail_send_mail import DmailSend


class Erc20BalanceModule(Module):
    module_name = 'ERC20_BALANCE_MODULE'
    module_config = 'erc20_balance'
    allowed_chains = ['ZKSYNC', 'LINEA', 'SCROLL', 'MANTA', 'BASE']
    cumulative_sum = 0

    def execute(self, token_address, chain, account):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        erc20_token = Erc20Token('LINEA', token_address, web3)

        balance = erc20_token.balance(account)

        self.cumulative_sum = self.cumulative_sum + balance.wei

        logger.info(f"{account.address} balance is {balance}")
        add_accumulator_balance("Total balance is", balance.wei)

    def log(self):
        return "ERC20 BALANCE"

    def get_contract_class(self):
        return DmailSend

    def parse_params(self, module_params):
        self.validate_supported_chain(module_params['chain'])

        return module_params['token_address'], module_params['chain']

    def order(self):
        return Order.RANDOM
