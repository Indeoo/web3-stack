import os

from loguru import logger

from sybil_engine.utils.duplicate_utils import check_duplicates
from sybil_engine.utils.package_import_utils import import_all_variables_from_directory
from sybil_engine.utils.config_utils import get_config


def load_scenario(args_module, module_map, modules_data):
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
    if get_config('shell_mode') == 'interactive':
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
        module_name = args_module
    scenario = modules_scenario_map[module_name]

    return scenario

def load_scenarios():
    scenarios_path = 'data/scenarios'
    if os.path.exists(scenarios_path) and os.path.isdir(scenarios_path):
        scenarios = import_all_variables_from_directory(scenarios_path)
        check_duplicates(scenarios, 'scenario_name')

        return scenarios
    else:
        return []


def get_module_name(module):
    if module[0] is not None:
        return module[0].module_name
    else:
        return 'SCENARIO'