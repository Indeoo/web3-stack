import random

from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.zks import ZKS
from web3_wizzard_lib.core.utils.sub_module import SubModule


class ZksDomain(SubModule):
    module_name = 'TAVAERA'

    def execute(self, account, chain='ZKSYNC'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['ZKS']
        zks = ZKS(contract_address, web3)

        domain_name = self.get_random_name(zks)

        zks.register(account, domain_name)

    def get_random_name(self, zks):
        domain_name = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(7, 15)))

        logger.info(f"Mint {domain_name}.zks domain")

        check_name = zks.available(domain_name)

        if check_name:
            return domain_name

        logger.info(f"{domain_name}.zks is unavailable, try another domain")

        return self.get_random_name(zks)

    def log(self):
        return "REGISTER RANDOM ZKS DOMAIN"
