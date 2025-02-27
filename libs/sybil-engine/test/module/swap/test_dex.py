import unittest

from eth_tester import EthereumTester, PyEVMBackend
from eth_utils import to_wei
from sybil_engine.domain.balance.tokens import Erc20Token
from web3 import Web3, EthereumTesterProvider
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.utils import SwapException
from test import init_set_test_config, test_account
from test.module.swap.mock_dex import MockFailDex
from test.test_config import setup_mock_eth_provider


class TestDex(unittest.TestCase):
    init_set_test_config()

    def test_succeed_after_3_retries(self, chain='MOCK_CHAIN'):
        chain_instance = get_chain_instance(chain)

        web3 = Web3(setup_mock_eth_provider())

        from_token = MockErc20Token(chain, 'ETH', web3)
        to_token = MockErc20Token(chain, 'USDC', web3)

        slippage = 0.99
        amount_to_swap = NativeBalance(from_eth_to_wei(1), chain, 'ETH')

        test_dex = MockFailDex(chain_instance, web3, 2, {'from': 0, 'to': 0})

        test_dex.swap(amount_to_swap, from_token, to_token, slippage, test_account)

    def test_fail_after_3_retries(self, chain='MOCK_CHAIN'):
        chain_instance = get_chain_instance(chain)

        web3 = Web3(setup_mock_eth_provider())

        from_token = MockErc20Token(chain, 'ETH', web3)
        to_token = MockErc20Token(chain, 'USDC', web3)
        slippage = 0.99
        amount_to_swap = NativeBalance(from_eth_to_wei(1), chain, 'ETH')

        test_dex = MockFailDex(chain_instance, web3, 3, {'from': 0, 'to': 0})

        with self.assertRaises(SwapException):
            test_dex.swap(amount_to_swap, from_token, to_token, slippage, test_account)


class MockErc20Token(Erc20Token):
    def __init__(self, chain, token, web3):
        super().__init__(chain, token, web3)

    def symbol(self):
        return self.token

    def address(self):
        return self.token
