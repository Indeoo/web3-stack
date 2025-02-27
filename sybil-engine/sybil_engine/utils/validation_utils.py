from sybil_engine.config.app_config import get_module_data
from sybil_engine.utils.utils import ConfigurationException

class ValidationException(Exception):
    def __init__(self, invalid_value, message, type=''):
        self.message = f'Invalid {type} value \'{invalid_value}\'. Possible values: {message}'
        super().__init__(self.message)


def validate_chain(chain):
    if not is_chain(chain):
        raise ValidationException(chain, f'Possible values: {get_module_data().get_supported_chains()}', type='chain')


def is_chain(chain_str):
    if not isinstance(chain_str, str):
        return False

    return chain_str in get_module_data().get_supported_chains()


def validate_interval(interval):
    if not is_interval(interval):
        raise ValidationException(interval, 'interval e.g: \'{\'from\': 1 \'to\': to}\'', type='interval')


def validate_amount_interval_possible_empty(interval):
    if interval == '':
        return

    validate_amount_interval(interval)


def validate_amount_interval(interval):
    if not (is_interval(interval) or interval == 'all_balance'):
        raise ValidationException(interval,
                                  'interval e.g: \'{\'from\': 0.01 \'to\': 0.09}\' or \'all_balance\'', type='amount')


def validate_refuel_interval(interval):
    if not (is_interval(interval) or interval == 'max'):
        raise ValidationException(interval,
                                  'interval e.g: \'{\'from\': 0.01 \'to\': 0.09}\' or \'max\'', type='refuel')


def is_interval(interval):
    if not isinstance(interval, dict):
        return False

    return has_required_keys(interval, ['from', 'to'])


def has_required_keys(value, required_keys):
    if not isinstance(value, dict):
        return False
    return all(key in value for key in required_keys)


def validate_token(token):
    if not is_token(token):
        raise ValidationException(token, 'USDC, ETH, WBTC etc.', type='token')


def is_token(token):
    if not isinstance(token, str):
        return False

    return True


def validate_dex_list(dex_list):
    if len(dex_list) == 0:
        raise ConfigurationException("Dex list is empty")

    dex_apps = get_module_data().get_swap_apps()

    for dex in dex_list:
        if not is_dex(dex):
            raise ValidationException(dex, dex_apps, type='dex')


def validate_dex(dex):
    dex_apps = get_module_data().get_swap_apps()

    if not is_dex(dex) and dex != 'random':
        raise ValidationException(dex, dex_apps, type='dex')


def is_dex(dex):
    if not isinstance(dex, str):
        return False

    return dex in get_module_data().get_swap_apps()
