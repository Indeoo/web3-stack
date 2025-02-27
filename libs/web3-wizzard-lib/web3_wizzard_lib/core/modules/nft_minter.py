import random

from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance, set_rpc_for_chain
from sybil_engine.module.module import RepeatableModule, Order
from sybil_engine.utils.package_import_utils import import_all_modules_in_directory, get_all_subclasses
from sybil_engine.utils.scan_utils import find_interacted_contracts
from sybil_engine.utils.utils import ConfigurationException, randomized_sleeping, RetryException, print_exception_chain
from sybil_engine.utils.validation_utils import validate_interval

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule
from web3_wizzard_lib.core.utils.sub_module import SubModule


class NFTMinter(RepeatableModule):
    module_name = 'NFT_MINTER'
    module_config = 'nft_minter'
    random_order = Order.RANDOM
    repeat_conf = 'nft_amount_interval'
    sleep_after_var = True
    retries = 100

    @RepeatableModule.repeatable_log
    def execute(self, nft_module_names, nft_amount_interval, unique_nft, skip_delay, account):
        self.sleep_after_var = True
        self.storage.setdefault("minted_nfts", [])
        minted_nfts = self.storage.get("minted_nfts")

        nft_modules_without_minted = [item for item in set(nft_module_names) if item not in minted_nfts]
        nfts = [nft for nft in self.get_nfts() if nft and nft.module_name in nft_modules_without_minted]

        if nft_amount_interval['to'] > len(nft_module_names):
            raise ConfigurationException(
                f"Interval {nft_amount_interval} to > amount of NFT nfts allowed {len(nft_module_names)}")

        inited_module = random.choice(nfts)()

        if unique_nft and not hasattr(inited_module, "allow_reuse_address"):
            chain = 'LINEA'
            interactions = find_interacted_contracts(
                account.address,
                get_chain_instance(chain)['api_scan'],
                get_chain_instance(chain)['api_scan_key']
            )

            nft_contract_address = self.get_nft_address(chain, inited_module)

            if nft_contract_address in interactions:
                logger.info(f"{inited_module.log()} already minted for {account.address}")
                self.sleep_after_var = False
                randomized_sleeping(skip_delay)
                return

        logger.info(f"Mint {inited_module.log()}")
        try:
            inited_module.execute(account)
        except SkipRetryException as e:
            self.sleep_after_var = False
            logger.info(e)
            return
        minted_nfts.append(inited_module.module_name)
        self.storage.put("minted_nfts", minted_nfts)

    def get_nfts(self):
        import_all_modules_in_directory("utils.modules.nft")
        return get_all_subclasses(SubModule) + get_all_subclasses(NftSubmodule)

    def get_nft_address(self, chain, inited_module):
        if inited_module.module_name in get_contracts_for_chain(chain):
            return get_contracts_for_chain(chain)[inited_module.module_name]
        else:
            return inited_module.nft_address

    def log(self):
        return "NFT MINTER"

    def parse_params(self, module_params):
        validate_interval(module_params['nft_amount_interval'])

        if 'skip_delay' not in module_params:
            module_params['skip_delay'] = {'from': 10, 'to': 30}

        if 'unique_nft' not in module_params:
            module_params['unique_nft'] = True

        return module_params['nft_modules'], module_params['nft_amount_interval'], module_params['unique_nft'], \
            module_params['skip_delay']

    retry_counter = 0

    def handle(self, e):
        print_exception_chain(e)

        if self.retry_counter < self.retries:
            self.retry_counter = self.retry_counter + 1
            logger.info(f"{self.retry_counter} retries from {self.retries}")
            set_rpc_for_chain('LINEA')
            randomized_sleeping({'from': 1, 'to': 60})
            raise RetryException(e)

    def sleep_after(self):
        return self.sleep_after_var


class SkipRetryException(Exception):
    pass
