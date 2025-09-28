from web3_wizzard_lib.core.sybil_engine.config.app_config import set_network
from web3_wizzard_lib.core.sybil_engine.module.modules import Modules
from test import MockFailModule
from web3_wizzard_lib.tests.core.sybil_engine.module.mock_module import MockModule
from test import RepeatableMockModule

module_map = {
    1000: (MockModule, 'mock_config'),
    1001: (MockFailModule, 'mock_fail_config'),
    1002: (RepeatableMockModule, 'repeatable_mock_config')
}

swap_apps = ['RepeatableMockModule', 'MockModule', 'MockFailModule']

test_modules = Modules(module_map, swap_apps)
set_network('LOCAL')