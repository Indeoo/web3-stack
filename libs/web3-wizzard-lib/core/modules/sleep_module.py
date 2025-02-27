import logging

from sybil_engine.module.module import Module
from sybil_engine.utils.utils import randomized_sleeping
from sybil_engine.utils.validation_utils import validate_amount_interval


class SleepModule(Module):
    module_name = 'SLEEP_MODULE'
    module_config = 'sleep_module_config'

    def execute(self, sleep_interval, account):
        logging.info("Additional sleeping module")
        randomized_sleeping(sleep_interval)

    def log(self):
        return "SLEEP MODULE"

    def sleep_after(self):
        return False

    def parse_params(self, module_params):
        validate_amount_interval(module_params['sleep_interval'])

        return [module_params['sleep_interval']]
