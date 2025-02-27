import unittest

from sybil_engine.module.execution_planner import create_execution_plans
from test import test_account
from test.test_config import create_config

mock_scenario = {
    'scenario_name': 'TEST_module_0_config',
    'scenario': [
        {
            'module': 'MockModule',
            'params': {
                'min_native_interval': {'from': 1, 'to': 1}
            }
        },
        {
            'module': 'RepeatableMockModule',
            'params': {
                'repeats': {'from': 3, 'to': 3}
            }
        },
        {
            'module': 'MockModule',
            'params': {
            }
        }
    ]
}


class TestExecutionPlanner(unittest.TestCase):

    def test_should_form_execution_planner(self, account=test_account):
        modules, encryption, min_native_interval, proxy_config, okx_config, sleep_interval, swap_retry_sleep_interval, gas_prices_gwei = create_config()

        execution_plans = create_execution_plans([account], min_native_interval, mock_scenario, modules)

        index, (plan_account, modules) = execution_plans[0]

        self.assertEqual(1, index)
        self.assertEqual(plan_account, account)
        self.assertEqual(5, len(modules))
        self.assertEqual(2000000000000000, modules[1][0].min_native_balance.wei)

    def test_should_form_execution_planner_with_min_native_interval(self, account=test_account):
        modules, encryption, min_native_interval, proxy_config, okx_config, sleep_interval, swap_retry_sleep_interval, gas_prices_gwei = create_config()

        execution_plans = create_execution_plans([account], min_native_interval, mock_scenario, modules)

        index, (plan_account, modules) = execution_plans[0]

        self.assertEqual(1, index)
        self.assertEqual(plan_account, account)
        self.assertEqual(5, len(modules))
        self.assertEqual(1000000000000000000, modules[0][0].min_native_balance.wei)
