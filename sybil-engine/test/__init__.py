import importlib
import pkgutil

from sybil_engine.config.app_config import set_network, set_dex_retry_interval, set_gas_prices
from sybil_engine.domain.balance.balance_utils import interval_to_eth_balance
from sybil_engine.utils.app_account_utils import create_app_account_with_proxies


test_account = create_app_account_with_proxies(
    ['0xb98308D11E2B578858Fbe65b793e71C7a0CAa43e'],
    False,
    'password',
    ['0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'],
    [],
    'RANDOM',
    ['0x6317842385f344acf68561f4e65f0f39e4fb4f1ad104b92bd007361aed39d8'],
)[0]

min_native_balance = interval_to_eth_balance({'from': 1, 'to': 1}, test_account, None, None)

global_vars = globals()

for loader, module_name, is_pkg in pkgutil.iter_modules(['core/contract']):
    module = importlib.import_module('.' + module_name, package='core.contract')
    global_vars[module_name] = module


gas_prices_gwei_test = {
    'ETH_MAINNET': 100,
    'MOCK_CHAIN': 100
}


def init_set_test_config():
    set_network('LOCAL')
    set_dex_retry_interval({'from': 0, 'to': 0})
    set_gas_prices(gas_prices_gwei_test)