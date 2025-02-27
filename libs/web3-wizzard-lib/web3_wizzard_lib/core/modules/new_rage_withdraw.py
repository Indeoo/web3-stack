from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.module.module import Module
from sybil_engine.utils.utils import ConfigurationException
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.new_rage_contract import NewRageContract


class NewRageModule(Module):
    module_name = 'NEW_RAGE_WITHDRAW'
    module_config = 'new_rage_config'

    def execute(self, token, account, chain='ARBITRUM'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, None)

        if token == 'USDC':
            contract_address = "0xf9305009FbA7E381b3337b5fA157936d73c2CF36"
        elif token == 'GLP':
            contract_address = "0x8478AB5064EbAC770DdCE77E7D31D969205F041E"
        else:
            raise ConfigurationException("No such token supported by Rage withdraw module")
        rage = NewRageContract(contract_address, web3)

        #balance = rage.balance_of(account)
        shares = rage.max_redeem(account)

        if shares > 0:
            logger.info(f"Withdraw  {shares} shares {token}")
            rage.redeem(account, shares)
        else:
            logger.info(f"Account {account.address} has 0 balance in Rage")

        #add_accumulator("Total rage withdraw", balance)

    def log(self):
        return "RAGE WITHDRAW"

    def parse_params(self, module_params):
        return module_params['token'],
