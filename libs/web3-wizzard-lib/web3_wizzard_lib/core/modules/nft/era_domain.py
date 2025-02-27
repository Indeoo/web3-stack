import random

from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.era_name import EraName
from web3_wizzard_lib.core.utils.sub_module import SubModule


class EraDomain(SubModule):
    nft_address = '0x935442AF47F3dc1c11F006D551E13769F12eab13'
    module_name = 'ERA_DOMAIN'

    def execute(self, account, chain='ZKSYNC'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['ERA']
        era_contract = EraName(contract_address, web3)

        domain_name = self.get_random_name(era_contract)

        era_contract.register(account, domain_name)

    def get_random_name(self, era_contract):
        domain_name = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(7, 15)))

        logger.info(f"Mint {domain_name}.era domain")

        check_name = era_contract.check_name(domain_name)

        if check_name:
            return domain_name

        logger.info(f"{domain_name}.era is unavailable, try another domain")

        return self.get_random_name(era_contract)

    def log(self):
        return "REGISTER RANDOM ERA NS DOMAIN"
