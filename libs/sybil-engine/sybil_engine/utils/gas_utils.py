import functools

from loguru import logger

from sybil_engine.data.networks import get_chain_instance

from sybil_engine.config.app_config import get_gas_prices
from sybil_engine.domain.balance.balance_utils import from_wei_to_gwei
from sybil_engine.utils.utils import randomized_sleeping

def l1_gas_price(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from sybil_engine.utils.web3_utils import init_web3
        web3_main = init_web3(get_chain_instance("ETH_MAINNET"), None)

        l1_max_gas_price = get_gas_prices()['ETH_MAINNET']

        check_gas_price(web3_main, l1_max_gas_price, 'L1')

        return func(*args, **kwargs)

    return wrapper


def check_gas_price(web3, max_gas_price_gwei, l1_or_l2):
    while True:
        try:
            gas_price_wei = web3.eth.gas_price
            if from_wei_to_gwei(gas_price_wei) > max_gas_price_gwei:
                raise GasPriceToHigh(
                    f"{l1_or_l2} Gas price is too high: {from_wei_to_gwei(gas_price_wei)}Gwei, max: {max_gas_price_gwei}Gwei")
            return
        except GasPriceToHigh as e:
            logger.info(e)
            randomized_sleeping({'from': 60 * 4, 'to': 60 * 8})


class GasPriceToHigh(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
