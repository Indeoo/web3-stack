from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance_utils import interval_to_erc20_balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.module.module import Module
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.utils import AccountException
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.zkdx_contract import ZKDXContract
from web3_wizzard_lib.core.contract.zkdx_data import ZKDXDataContract


class ZKDX(Module):
    module_name = 'ZKDX'
    module_config = 'zkdx_config'

    def execute(self, action, amount_interval, account: AppAccount, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        zkdx_contract = get_contracts_for_chain(chain)['ZKDX']
        zkdx_data_contract = get_contracts_for_chain(chain)['ZKDX_DATA']

        zkdx = ZKDXContract(zkdx_contract, web3)

        if action == 'DEPOSIT':
            amount = interval_to_erc20_balance(amount_interval, account, 'USDC', chain, web3)

            erc20 = Erc20Token(chain, 'USDC', web3)

            if erc20.allowance(account, zkdx_contract) < erc20.balance(account).wei:
                erc20.approve(account, zkdx_contract)

            logger.info(f"Deposit {amount} to ZKDX")
            zkdx.swap_to_zkdx(account, amount)
        if action == 'WITHDRAW':
            zkdx_data = ZKDXDataContract(zkdx_data_contract, web3)
            balance = zkdx_data.get_balance(account)[0]

            if balance == 0:
                raise AccountException("ZKDX Balance is 0, skip")

            logger.info(f"WITHDRAW {balance / 10 ** 18} ZUSD to ZKDX")
            zkdx.swap_from_zkdx(account, balance)
        else:
            raise Exception(f"{action} action not supported")

    def log(self):
        return "ZKDX"

    def parse_params(self, module_params):
        return [
            module_params['action'],
            module_params['amount_interval']
        ]


class EmptyDepositException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
