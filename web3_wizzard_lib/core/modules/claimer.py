from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.module.module import Module
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.claims.layerzero_claimer import claimer_zro
from web3_wizzard_lib.core.modules.claims.rabby_claimer import claimer_rabby

native_prices = {
    'ETH': 3700,
    'USDT': 1
}


class Claimer(Module):
    module_name = 'CLAIMER'
    sleep_after_conf = True
    module_config = 'claimer_config'

    def execute(self, chain, layerzero_token, project, account: AppAccount):
        logger.info(f"CLAIM L0 tokens for {account} on {chain}")
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, None)

        if project == 'ZRO':
            claimer_zro(account, chain_instance, layerzero_token, web3)
        else:
            claimer_rabby(account, web3)

    def log(self):
        return "CLAIMER"

    def parse_params(self, module_params):
        if 'project' not in module_params:
            module_params['project'] = 'ZRO'

        return [
            module_params['chain'],
            module_params['token'],
            module_params['project']
        ]

    def sleep_after(self):
        return self.sleep_after_conf
