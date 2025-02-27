import argparse
import os

from eth_tester import EthereumTester, PyEVMBackend
from eth_utils import to_wei
from web3 import EthereumTesterProvider

from test import test_account
from test.module.test_modules import test_modules

cdir = os.getcwd()
proxy_file = f'{cdir}/tests/proxy.txt'
args = argparse.Namespace(password='test', private_keys=f'{cdir}/tests/private_keys.txt',
                          cex_addresses=f'{cdir}/tests/cex_addresses.txt',
                          starknet_addresses=f'{cdir}/tests/starknet_addresses.txt',
                          proxy_file=f'{cdir}/tests/proxy.txt',
                          network='LOCAL')

sleep_interval = {'from': 0, 'to': 0}
swap_retry_sleep_interval = {'from': 0, 'to': 0}
encryption = False
warmup_allowed_dex = ['syncswap', 'mute', 'velocore']


def scenario_from_module(module_config, scenario_name):
    return {
        'scenario_name': scenario_name,
        'scenario': [
            module_config
        ]
    }


def create_config():
    encryption = False
    password = 'test'  # if encryption False then password is ignored

    proxy_mode = 'RANDOM'  # RANDOM, STRICT

    # Gwei Price Limits
    gas_prices = {
        'ETH_MAINNET': 25,
        'MOCK_CHAIN': 0.26,
    }

    # CEX configuration !!!CURRENTLY ONLY FOR ZKSYNC!!!
    cex_data = ''
    auto_withdrawal = False
    withdraw_interval = {'from': 0.01, 'to': 0.015}

    min_native_interval = {'from': 0.002, 'to': 0.002}

    okx_config = (cex_data, auto_withdrawal, withdraw_interval)

    return test_modules, encryption, min_native_interval, proxy_mode, okx_config, sleep_interval, swap_retry_sleep_interval, gas_prices


def setup_mock_eth_provider():
    DEFAULT_INITIAL_BALANCE = to_wei(10000, 'ether')
    MOCK_ADDRESS = bytes.fromhex(test_account.address[2:])

    GENESIS_STATE = {
        MOCK_ADDRESS: {
            "balance": DEFAULT_INITIAL_BALANCE,
            "nonce": 0,
            "code": b'',
            "storage": {}
        }
    }

    eth_tester = EthereumTester(backend=PyEVMBackend(genesis_state=GENESIS_STATE))

    return EthereumTesterProvider(eth_tester)