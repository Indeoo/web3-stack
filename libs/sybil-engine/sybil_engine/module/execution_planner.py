import itertools
import random

from sybil_engine.domain.account_storage import AccountStorage
from sybil_engine.domain.balance.balance_utils import interval_to_native_balance
from sybil_engine.module.module import RepeatableModule, Order
from sybil_engine.utils.utils import interval_to_int, ConfigurationException


def create_execution_plans(accounts, min_native_interval, module_config, modules_data):
    execution_plan = []

    for index, account in enumerate(accounts, 1):
        modules = randomize_modules(get_account_modules(min_native_interval, account, module_config, modules_data))

        execution_plan.append((index, (account, modules)))

    return execution_plan


def get_account_modules(default_min_native_interval, account, module_config, modules_data):
    storage = AccountStorage()

    module_classes = [
        (modules_data.get_module_class_by_name(module['module']), module['params']) for module in
        module_config['scenario']
    ]

    modules = []

    for module_class, module_args in module_classes:
        min_native_interval = get_min_native_interval(default_min_native_interval, module_args)

        if issubclass(module_class, RepeatableModule):
            counted_repeats = repeats(module_args, module_class.repeat_conf)
            for i in counted_repeats:
                min_native_balance = interval_to_native_balance(min_native_interval, account, None, None)
                module_with_args = (module_class(min_native_balance, storage, len(counted_repeats)), module_args)
                modules.append(module_with_args)
        else:
            min_native_balance = interval_to_native_balance(min_native_interval, account, None, None)
            module_with_args = (module_class(min_native_balance, storage), module_args)
            modules.append(module_with_args)

        for module, module_args in modules:
            try:
                module.parse_params(module_args)
            except Exception as e:
                raise ConfigurationException(f"Error in {module.module_name} configuration") from e
    return modules


def repeats(module_params, repeat_conf):
    if repeat_conf not in module_params:
        return range(1)
    else:
        return range(interval_to_int(module_params[repeat_conf]))


def split_list(items):
    result = []
    sublist = []
    for module, config in items:
        item_tuple = (module, config)
        if 'order' in config:
            order = Order.__members__[config['order']]
        else:
            order = module.order()

        if order == Order.STRICT:
            if sublist:
                result.append(sublist)
                sublist = []
            result.append([item_tuple])
        else:
            sublist.append(item_tuple)
    if sublist:
        result.append(sublist)
    return result


def randomize_modules(modules):
    arrays = split_list(modules)
    [random.shuffle(array) for array in arrays]
    return list(itertools.chain(*arrays))


def get_min_native_interval(default_min_native_interval, module_params):
    if 'min_native_interval' in module_params:
        return module_params['min_native_interval']
    else:
        return default_min_native_interval
