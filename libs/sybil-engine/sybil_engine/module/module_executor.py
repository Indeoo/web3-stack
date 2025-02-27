from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain

from sybil_engine.data.networks import get_chain_instance

from sybil_engine.utils.accumulator import add_accumulator_str, remove_accumulator_str
from sybil_engine.utils.scan_utils import find_interacted_contracts, find_interacted_data
from sybil_engine.utils.utils import randomized_sleeping, ModuleException, print_exception_chain, \
    ConfigurationException, RetryException


class ModuleExecutor:
    def execute_modules(self, modules, account, sleep_interval):
        try:
            for module, module_args in modules:
                self.execute_module(module_args, account, module, sleep_interval)
            add_accumulator_str("Finished accounts: ", account)
            remove_accumulator_str("Pending accounts: ", account)
        except ConfigurationException as e:
            raise Exception(f"Configuration error in {module.module_name}: {e}") from e
        except Exception as e:
            logger.error(f'Error, skip {account}:')
            print_exception_chain(e)
            add_accumulator_str("Failed accounts: ", account)

    def execute_module(self, module_args, account, module, sleep_interval):
        try:
            args = list(module_args.keys())
            if 'unique' in args and 'chain' in args and module_args['unique']:
                chain = module_args['chain']
                chain_instance = get_chain_instance(chain)

                interactions = find_interacted_contracts(
                    account.address,
                    chain_instance['api_scan'],
                    chain_instance['api_scan_key']
                )

                data = find_interacted_data(
                    account.address,
                    chain_instance['api_scan'],
                    chain_instance['api_scan_key']
                )

                if 'contract' in args:
                    contract_address = module_args['contract']
                elif module.module_name == 'SEND_TO_CEX':
                    contract_address = account.cex_address
                else:
                    contract_address = get_contracts_for_chain(chain)[module.module_name]

                if contract_address in interactions and data in interactions:
                    logger.info(f"{module.log()} already minted for {account.address}")
                    return

            parsed_module_args = module.parse_params(module_args)
            try:
                module.execute(*parsed_module_args, account)
                if module.sleep_after():
                    randomized_sleeping(sleep_interval)
            except Exception as e:
                module.handle(e)
        except RetryException as e:
            self.execute_module(module_args, account, module, sleep_interval)
        except ModuleException as e:
            print_exception_chain(e)
