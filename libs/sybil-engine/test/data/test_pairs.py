import unittest

from sybil_engine.data.pairs import Pairs
from test import init_set_test_config


class TestPairs(unittest.TestCase):
    init_set_test_config()

    # def test_get_pairs_by_tokens(self):
    #     pair = Pairs(swap_facade)
    #
    #     pairs = pair.get_pairs_by_tokens('ETH', 'USDC', 'LINEA')
    #
    #     self.assertEqual(
    #         4,
    #         len(pairs)
    #     )
    #
    #     pairs_with_swap = pair.get_pairs_by_tokens('ETH', 'USDC', 'LINEA', 'syncswap')
    #
    #     self.assertEqual(
    #         len(pairs_with_swap),
    #         1
    #     )
    #
    #     pairs_with_swaps = pair.get_pairs_by_tokens('ETH', 'USDC', 'LINEA', ['syncswap', 'pancake'])
    #
    #     self.assertEqual(
    #         len(pairs_with_swaps),
    #         2
    #     )
    #
    # def test_get_swap_apps_by_pair(self):
    #     pair = Pairs(swap_facade)
    #
    #     self.assertIn(
    #         'odos',
    #         pair.get_swap_apps_by_pair('ETH', 'USDC', 'ZKSYNC')
    #     )
    #     self.assertNotIn(
    #         'lineaswap',
    #         pair.get_swap_apps_by_pair('ETH', 'USDC', 'ZKSYNC')
    #     )
    #     self.assertNotIn(
    #         'horizondex',
    #         pair.get_swap_apps_by_pair('ETH', 'USDT', 'ZKSYNC')
    #     )
    #     self.assertNotIn(
    #         'horizondex',
    #         pair.get_swap_apps_by_pair('ETH', 'USDT', 'BASE')
    #     )
