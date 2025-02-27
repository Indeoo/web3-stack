import random
from typing import Optional, Any

from sybil_engine.config.app_config import get_network
import requests
from eth_tester import EthereumTester, PyEVMBackend
from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from web3 import Web3, EthereumTesterProvider

from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance_utils import get_native_balance, find_chain_with_max_usdc, \
    find_chain_with_max_native
from sybil_engine.domain.balance.tokens import Erc20Token


def init_web3(chain_instance, proxy: Optional[Any]):
    # Define retry strategy
    retry_strategy = Retry(
        total=5,  # Total number of retries to allow
        status_forcelist=[429, 443, 500, 502, 503, 504],  # Status codes to retry for
        allowed_methods=["HEAD", "GET", "POST"],  # HTTP methods to retry
        backoff_factor=3,  # Backoff factor to apply between attempts
    )

    # Create a session with the retry strategy
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    if proxy is not None:
        provider = Web3.HTTPProvider(chain_instance['rpc'], request_kwargs={"proxies": {'https': proxy, 'http': proxy}},
                                     session=session)
    else:
        provider = Web3.HTTPProvider(endpoint_uri=chain_instance['rpc'], session=session)

    # if get_network() == 'LOCAL':
    #     eth_tester = EthereumTester(PyEVMBackend())
    #     provider = EthereumTesterProvider(eth_tester)

    web3 = Web3(provider=provider)

    if chain_instance['poa']:
        from web3.middleware import GasPriceStrategyMiddleware
        web3.middleware_onion.inject(GasPriceStrategyMiddleware, layer=0)

    return web3


def log_retry(retry_state):
    # Log the retry attempt number and the delay before the next retry
    logger.info(f"Retry attempt: {retry_state.retry_count}. Delaying for {retry_state.backoff} seconds before next retry.")



def get_amount_to_bridge_usdc(bridge_amount_interval):
    if bridge_amount_interval['from'] > bridge_amount_interval['to']:
        raise Exception('Invalid bridge interval')

    return int(
        random.randint(bridge_amount_interval['from'] * 10 ** 2, bridge_amount_interval['to'] * 10 ** 2)) * 10 ** 4


def print_account_data(account_data):
    for chain, usdc, native_balance, web3 in account_data:
        logger.info(f"{chain}: {usdc.log_line()}, {native_balance.log_line()}")


def get_all_account_data(account, chains):
    balances = []
    for chain in chains:
        web3 = init_web3(get_chain_instance(chain), account.proxy)
        native_balance = get_native_balance(account, web3, get_chain_instance(chain))

        erc20_from_token = Erc20Token(chain, 'USDC', web3)

        erc20_balance = erc20_from_token.balance(account)

        balances = balances + [(chain, erc20_balance, native_balance, web3)]

    return balances


def get_max_balance_data(token_type, chains, account):
    data = get_all_account_data(account, chains)
    print_account_data(data)

    if token_type == 'USDC':
        return find_chain_with_max_usdc(data)
    else:
        return find_chain_with_max_native(data)
