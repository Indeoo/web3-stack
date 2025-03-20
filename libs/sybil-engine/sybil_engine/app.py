import os

from loguru import logger

from sybil_engine.config.app_config import set_network, set_gas_prices, set_dex_retry_interval, set_module_data, \
    set_cex_data, set_cex_conf
from sybil_engine.module.execution_planner import create_execution_plans
from sybil_engine.module.module_executor import ModuleExecutor
from sybil_engine.utils.accumulator import print_accumulated, add_accumulator_str, add_accumulator
from sybil_engine.utils.app_account_utils import create_app_account
from sybil_engine.utils.arguments_parser import parse_arguments, parse_profile
from sybil_engine.utils.configuration_loader import load_config_maps
from sybil_engine.utils.fee_storage import print_fee
from sybil_engine.utils.logs import load_logger
from sybil_engine.utils.telegram import send_to_bot
from sybil_engine.utils.config_utils import add_config, get_config
from sybil_engine.utils.utils import ConfigurationException
from sybil_engine.scenario_loader import load_scenario


def launch_with_data(modules_data, config_map=None, module_map=None):
    if config_map is None or module_map is None:
        profile = parse_profile()
        loaded_config_map, loaded_module_map = load_config_maps(profile)

        if config_map is None:
            config_map = loaded_config_map

        if module_map is None:
            module_map = loaded_module_map

    __setup_default_config(config_map)

    load_logger(send_to_bot, config_map['telegram_enabled'], config_map['telegram_log_level'])
    add_config("STATISTICS_MODE", config_map['statistic_config']['mode'])
    add_config("STATS_SPREADSHEET_ID", config_map['statistic_config']['spreadsheet_id'])

    for k, v in config_map.items():
        add_config(k, v)

    for k, v in module_map.items():
        add_config(k, v)

    args = parse_arguments()

    for k, v in args.items():
        add_config(k, v)

    scenario = load_scenario(get_config('module'), module_map, modules_data)

    config = (
        modules_data,
        get_config('encryption'),
        module_map['min_native_interval'],
        get_config('proxy_mode'),
        get_config('cex_data'),
        module_map['sleep_interval'],
        module_map['swap_retry_sleep_interval'],
        get_config('gas_prices'),
        get_config('account_creation_mode'),
        get_config('cex_address_validation'),
        get_config('interactive_confirmation'),
        get_config('password').encode('utf-8')
    )

    launch_app(scenario, config)


def __setup_default_config(config_map):
    data_folder = 'data'
    wallets_folder = f'{data_folder}/wallets'

    defaults = {
        'module': os.environ.get('MODULE', ''),
        'spreadsheet_id': os.environ.get('SPREADSHEET_ID', ''),
        'encryption': False,
        'shell_mode': 'classic',
        'proxy_mode': 'RANDOM',
        'account_creation_mode': 'TXT',
        'password': os.environ.get('PASSWORD', 'test'),
        'profile': os.environ.get('PROFILE', 'default'),
        'cex_address_validation': False,
        'interactive_confirmation': False,
        'statistic_config': {
            'mode': 'CSV',
            'spreadsheet_id': '',
        },
        'wallets': os.environ.get('WALLETS', wallets_folder),
        'private_keys': os.environ.get('PRIVATE_KEYS', f'{wallets_folder}/private_keys.txt'),
        'cex_addresses': os.environ.get('CEX_ADDRESSES', f'{wallets_folder}/cex_addresses.txt'),
        'starknet_addresses': os.environ.get('STARKNET_ADDRESSES', f'{wallets_folder}/starknet_addresses.txt'),
        'proxy_file': os.environ.get('PROXY_FILE', f'{wallets_folder}/proxy.txt'),
        'cex_conf': os.environ.get('CEX_CONF', 'cex'),
        'network': os.environ.get('NETWORK', 'MAIN'),
        'account_csv': os.environ.get('ACCOUNT_CSV', f'{wallets_folder}/accounts.csv'),
        'telegram_enabled': False,
        'telegram_api_key': '',
        'telegram_api_chat_id': 1,
        'telegram_log_level': 'ERROR',  # ['INFO', 'ERROR', 'DEBUG']
    }

    for key, value in defaults.items():
        config_map.setdefault(key, value)


def launch_app(scenario, config):
    (modules_data, encryption, min_native_interval, proxy_mode, cex_data, sleep_interval, swap_retry_sleep_interval,
     gas_price, account_creation_mode, cex_address_validation, interactive_confirmation, password) = config

    set_network(get_config('network'))
    set_dex_retry_interval(swap_retry_sleep_interval)
    set_gas_prices(gas_price)
    set_module_data(modules_data)
    set_cex_data((password, cex_data))
    set_cex_conf(get_config('cex_conf'))

    logger.info(f"START {scenario['scenario_name']} module in {get_config("network")}")

    profile = parse_profile()
    logger.info(f"Profile {profile} activated")

    if not all(modules_data.get_module_class_by_name(module['module']) for module in scenario['scenario']):
        raise ConfigurationException("Non-existing module is used")

    accounts = create_app_account(encryption, proxy_mode, account_creation_mode, cex_address_validation)
    add_accumulator("Acc Amount", len(accounts))

    execution_plans = create_execution_plans(accounts, min_native_interval, scenario, modules_data)

    if interactive_confirmation:
        logger.info("Are you sure you want to start with this configuration? Y/n")
        choice = input()
        if choice != "Y":
            logger.info("Exiting")
            return

    try:
        __proceed_accounts(accounts, execution_plans, sleep_interval)
    finally:
        print_fee()
        print_accumulated()


def __proceed_accounts(accounts, execution_plans, sleep_interval):
    for account in accounts:
        add_accumulator_str("Pending accounts: ", account)

    for index, (account, modules) in execution_plans:
        logger.info(f"[{index}/{len(accounts)}][{account.app_id}] {account.address}")
        ModuleExecutor().execute_modules(modules, account, sleep_interval)
