from sybil_engine.config.app_config import get_network
from sybil_engine.data.networks import get_networks
from sybil_engine.module.module import Module, RepeatableModule


class Modules:
    def __init__(self, module_map, swap_facade):
        self.swap_facade = swap_facade

    def get_module_config_by_name(self, module_name, module_map):
        for key, (module_class, config) in self.get_module_map().items():
            if module_class and (module_class.module_name == module_name):
                if config is None:
                    return {}
                elif isinstance(config, str):
                    if config in module_map:
                        return module_map[config]
                    else:
                        return "{}"
                else:
                    return config
        return 0

    def get_module_class_by_name(self, module_name):
        for key, (module_class, config) in self.get_module_map().items():
            if module_class and (module_class.module_name == module_name):
                return module_class
        return 0

    def get_modules(self):
        return [module[0] for module in self.get_module_map().values()]

    def get_module_map(self):
        module_map = {}
        for cls in Module.__subclasses__() + RepeatableModule.__subclasses__():
            if cls.__name__ != "RepeatableModule":
                module_map[cls.module_name] = (cls, cls.module_config)
        return module_map

    def get_swap_apps(self):
        return self.swap_facade.get_swap_apps()

    def get_supported_chains(self):
        return list(get_networks(get_network()).copy().keys())
