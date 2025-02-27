import os

from loguru import logger

from sybil_engine.config.app_config import set_network, set_gas_prices, set_dex_retry_interval, set_module_data, \
    set_cex_data, set_cex_conf
from sybil_engine.module.execution_planner import create_execution_plans
from sybil_engine.module.module_executor import ModuleExecutor
from sybil_engine.utils.accumulator import print_accumulated, add_accumulator_str, add_accumulator
from sybil_engine.utils.app_account_utils import create_app_account
from sybil_engine.utils.arguments_parser import parse_arguments, parse_profile
from sybil_engine.utils.configuration_loader import load_config_maps, load_module_vars
from sybil_engine.utils.duplicate_utils import check_duplicates
from sybil_engine.utils.fee_storage import print_fee
from sybil_engine.utils.logs import load_logger
from sybil_engine.utils.package_import_utils import import_all_variables_from_directory
from sybil_engine.utils.telegram import set_telegram_api_chat_id, set_telegram_api_key, send_to_bot, add_config
from sybil_engine.utils.utils import ConfigurationException
import pkgutil
import importlib


def prepare_launch_without_data(modules_package):
    package = importlib.import_module(modules_package)

    for loader, module_name, is_pkg in pkgutil.walk_packages(path=package.__path__):
        if not is_pkg:
            importlib.import_module('.' + module_name, package=modules_package)

    modules_data = load_module_vars(modules_package)['modules_data']
    launch_with_data(modules_data)


def launch_with_data(modules_data):
    config_map, module_map = load_config_maps()

    load_logger(send_to_bot, config_map['telegram_enabled'], config_map['telegram_log_level'])

    set_telegram_api_chat_id(config_map['telegram_api_chat_id'])
    set_telegram_api_key(config_map['telegram_api_key'])

    add_config("STATISTICS_MODE", "CSV")

    if "statistic_config" in config_map:
        if "mode" in config_map['statistic_config']:
            add_config("STATISTICS_MODE", config_map['statistic_config']['mode'])
        if "spreadsheet_id" in config_map['statistic_config']:
            add_config("SPREADSHEET_ID", config_map['statistic_config']['spreadsheet_id'])

    setup_default_config(config_map)

    args = parse_arguments(config_map['password'], config_map['spreadsheet_id'], module_map['module'])

    try:
        scenario = load_scenario(args, config_map, module_map, modules_data)
    except ValueError as e:
        return

    config = (
        modules_data,
        config_map['encryption'],
        module_map['min_native_interval'],
        config_map['proxy_mode'],
        config_map['cex_data'],
        module_map['sleep_interval'],
        module_map['swap_retry_sleep_interval'],
        config_map['gas_prices'],
        config_map['account_creation_mode'],
        config_map['cex_address_validation'],
        config_map['interactive_confirmation']
    )

    launch_app(args, scenario, config)


def setup_default_config(config_map):
    defaults = {
        'shell_mode': 'classic',
        'account_creation_mode': 'TXT',
        'cex_address_validation': False,
        'interactive_confirmation': True,
        'spreadsheet_id': None
    }

    for key, value in defaults.items():
        config_map.setdefault(key, value)


def load_scenario(args, config_map, module_map, modules_data):
    modules = []

    for module in modules_data.get_modules():
        module_name = module.module_name
        modules.append(
            {
                'scenario_name': module_name,
                'scenario': [
                    {'module': module_name, 'params': modules_data.get_module_config_by_name(module_name, module_map)}]
            }
        )
    modules_scenario_map = {
        module_scenario['scenario_name']: module_scenario for module_scenario in
        load_scenarios() + modules
    }
    if config_map['shell_mode'] == 'interactive':
        logger.info("Choose module (by id) or scenario (by name):")

        for module_id, module in modules_data.get_module_map().items():
            module_name = get_module_name(module)
            logger.info(f"  {module_id} {module_name}")

        for scenario in load_scenarios():
            logger.info(f"  {scenario['scenario_name']}")

        choice = input()

        if choice.isdigit():
            selected_module = modules_data.get_module_map()[int(choice)]
            module_name = get_module_name(selected_module)
        else:
            module_name = choice
    else:
        module_name = args.module
    scenario = modules_scenario_map[module_name]

    return scenario


def get_module_name(module):
    if module[0] is not None:
        return module[0].module_name
    else:
        return 'SCENARIO'


def launch_app(args, module_config, config):
    (modules_data, encryption, min_native_interval, proxy_mode, cex_data, sleep_interval, swap_retry_sleep_interval,
     gas_price, account_creation_mode, cex_address_validation, interactive_confirmation) = config

    set_network(args.network)
    set_dex_retry_interval(swap_retry_sleep_interval)
    set_gas_prices(gas_price)
    set_module_data(modules_data)
    set_cex_data((args.password.encode('utf-8'), cex_data))
    set_cex_conf(args.cex_conf)

    logger.info(f"START {module_config['scenario_name']} module in {args.network}")

    profile = parse_profile().profile
    logger.info(f"Profile {profile} activated")

    if not all(modules_data.get_module_class_by_name(module['module']) for module in module_config['scenario']):
        raise ConfigurationException("Non-existing module is used")

    accounts = create_app_account(args, encryption, proxy_mode, account_creation_mode, cex_address_validation)
    add_accumulator("Acc Amount", len(accounts))

    execution_plans = create_execution_plans(accounts, min_native_interval, module_config, modules_data)

    if interactive_confirmation:
        logger.info("Are you sure you want to start with this configuration? Y/n")
        choice = input()
        if choice != "Y":
            logger.info("Exiting")
            return

    try:
        proceed_accounts(accounts, execution_plans, sleep_interval)
    finally:
        print_fee()
        print_accumulated()


def proceed_accounts(accounts, execution_plans, sleep_interval):
    for account in accounts:
        add_accumulator_str("Pending accounts: ", account)

    for index, (account, modules) in execution_plans:
        logger.info(f"[{index}/{len(accounts)}][{account.app_id}] {account.address}")
        ModuleExecutor().execute_modules(modules, account, sleep_interval)


def load_scenarios():
    scenarios_path = 'data/scenarios'
    if os.path.exists(scenarios_path) and os.path.isdir(scenarios_path):
        scenarios = import_all_variables_from_directory(scenarios_path)
        check_duplicates(scenarios, 'scenario_name')

        return scenarios
    else:
        return []
