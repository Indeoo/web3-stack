import unittest

from sybil_engine.config.app_config import set_module_data
from sybil_engine.utils.validation_utils import validate_chain, ValidationException
from test.module.test_modules import test_modules


class TestValidation(unittest.TestCase):

    def test_shouldValidateValidChain(self):
        set_module_data(test_modules)

        try:
            #validate_chain('ZKSYNC')
            validate_chain('MOCK_CHAIN')
        except Exception as e:
            self.fail(e)

    def test_shouldFailInInvalidChain(self):
        set_module_data(test_modules)

        with self.assertRaises(Exception):
            ValidationException('INVALID_CHAIN')
