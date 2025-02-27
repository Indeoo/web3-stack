import importlib.util
import os
import pkgutil
import sys


def import_all_variables_from_directory(directory_path):
    scenarios = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module_path = os.path.join(directory_path, filename)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            for var_name in dir(module):
                if not var_name.startswith('_'):
                    scenario = getattr(module, var_name)
                    scenarios.append(scenario)

    return scenarios

def import_all_modules_in_directory(package_name):
    package = importlib.import_module(package_name)
    package_path = package.__path__[0]
    for _, module_name, _ in pkgutil.iter_modules([package_path]):
        full_module_name = f"{package_name}.{module_name}"
        importlib.import_module(full_module_name)

def get_all_subclasses(cls):
    subclasses = cls.__subclasses__()
    for subclass in subclasses:
        subclasses.extend(get_all_subclasses(subclass))
    return subclasses