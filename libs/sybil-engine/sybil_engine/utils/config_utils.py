from sybil_engine.utils.utils import ConfigurationException


app_configuration = {}

def add_config(key, value):
    global app_configuration
    app_configuration[key] = value


def get_config(key):
    global app_configuration

    if key not in app_configuration:
        raise ConfigurationException(f"Config key {key} is not defined")
    return app_configuration[key]
