from loguru import logger
from sybil_engine.module.module import RepeatableModule


class RepeatableMockModule(RepeatableModule):
    module_name = 'RepeatableMockModule'

    def __init__(self, min_native_balance, storage, repeats):
        super().__init__(min_native_balance, storage, repeats)

    def execute(self, account):
        logger.info("SuccessModule")

    def log(self):
        return "TEST FAIL MODULE"
