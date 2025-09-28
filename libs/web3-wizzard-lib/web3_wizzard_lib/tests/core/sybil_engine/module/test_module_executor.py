import unittest

from web3_wizzard_lib.core.sybil_engine.module.module_executor import ModuleExecutor
from web3_wizzard_lib.core.sybil_engine.utils.accumulator import get_value
from web3_wizzard_lib.core.sybil_engine.utils.utils import AccountException
from test import test_account
from test import MockFailModule
from web3_wizzard_lib.tests.core.sybil_engine.module.mock_module import MockModule
from test import MockNotEnoughNativeModule
from test import RepeatableMockModule


class TestModuleExecutor(unittest.TestCase):

    def test_execute_module(self):
        sleep_interval = {'from': 0, 'to': 0}
        account = test_account
        min_native_balance = {'from': 0.001, 'to': 0.001}
        modules = [
            (MockModule(min_native_balance, None), {}),
            (MockModule(min_native_balance, None), {}),
            (MockModule(min_native_balance, None), {})
        ]

        ModuleExecutor().execute_modules(modules, account, sleep_interval)

        self.assertEqual(get_value("Finished accounts: "), [test_account])

    def test_shouldThrowNotEnoughNativeBalance(self):
        sleep_interval = {'from': 0, 'to': 0}
        account = test_account
        min_native_balance = {'from': 0.001, 'to': 0.001}
        modules = [
            (MockModule(min_native_balance, None), {}),
            (MockModule(min_native_balance, None), {}),
            (MockNotEnoughNativeModule(min_native_balance, None), {})
        ]

        ModuleExecutor().execute_modules(modules, account, sleep_interval)

        self.assertEqual(len(get_value("Failed accounts: ")), 1)

    def test_should_throwAccountExceptionOnModuleException(self):
        sleep_interval = {'from': 0, 'to': 0}
        account = test_account
        min_native_balance = {'from': 0.001, 'to': 0.001}

        module = MockFailModule(min_native_balance, None)

        with self.assertRaises(AccountException):
            ModuleExecutor().execute_module({}, account, module, sleep_interval)

    def test_should_throwHandleExceptionOnRepeatableModuleException(self):
        sleep_interval = {'from': 0, 'to': 0}
        account = test_account
        min_native_balance = {'from': 0.001, 'to': 0.001}

        module = RepeatableMockModule(min_native_balance, None, 1)

        ModuleExecutor().execute_module({}, account, module, sleep_interval)
