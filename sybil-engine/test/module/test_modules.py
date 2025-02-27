from sybil_engine.config.app_config import set_network
from sybil_engine.module.modules import Modules
from test.module.mock_fail_module import MockFailModule
from test.module.mock_module import MockModule
from test.module.repeatable_mock_module import RepeatableMockModule

module_map = {
    1000: (MockModule, 'mock_config'),
    1001: (MockFailModule, 'mock_fail_config'),
    1002: (RepeatableMockModule, 'repeatable_mock_config')
}

swap_apps = ['RepeatableMockModule', 'MockModule', 'MockFailModule']

test_modules = Modules(module_map, swap_apps)
set_network('LOCAL')