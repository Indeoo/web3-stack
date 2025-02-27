network = None
dex_retry_interval = None
gas_prices_gwei = None
module_data = None
cex_data = None, None, None
cex_conf = None


def set_network(value):
    global network
    network = value


def get_network():
    return network


def set_dex_retry_interval(value):
    global dex_retry_interval
    dex_retry_interval = value


def get_dex_retry_interval():
    return dex_retry_interval


def set_gas_prices(value):
    global gas_prices_gwei
    gas_prices_gwei = value


def get_gas_prices():
    return gas_prices_gwei


def set_module_data(value):
    global module_data
    module_data = value


def get_module_data():
    return module_data


def set_cex_data(value):
    global cex_data
    cex_data = value


def get_cex_data():
    return cex_data


def set_cex_conf(value):
    global cex_conf
    cex_conf = value


def get_cex_conf():
    return cex_conf