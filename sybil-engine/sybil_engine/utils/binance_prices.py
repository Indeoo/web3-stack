import requests

from sybil_engine.config.app_config import get_network
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei


def get_binance_price(symbol):
    if get_network() != 'MAIN':
        return 1

    BASE_URL = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": symbol}

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return float(data['price'])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def get_amount_out_from_eth(amount_to_swap, from_token, to_token, slippage):
    return int(get_binance_price(from_token + to_token) * slippage * float(amount_to_swap.readable()) * 1000000)


def get_amount_out_to_eth(amount_to_swap, from_token, to_token, slippage):
    return from_eth_to_wei(float(amount_to_swap.readable()) / get_binance_price(to_token + from_token) * slippage)
