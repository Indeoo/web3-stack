import importlib.util

from sybil_engine.utils.arguments_parser import parse_profile


def load_module_vars(filename):
    spec = importlib.util.spec_from_file_location("module.name", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return vars(module)


def load_config_maps():
    profile = parse_profile().profile
    try:
        config_map = load_module_vars(f'data/config_{profile}.py')
    except FileNotFoundError as e:
        raise Exception(f'config for profile {profile} not found') from e

    try:
        module_map = load_module_vars(f'data/module_config_{profile}.py')
    except FileNotFoundError as e:
        raise Exception(f'module_config for profile {profile} not found') from e

    return config_map, module_map
