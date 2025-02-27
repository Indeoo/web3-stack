import unittest

from sybil_engine.data.exception import NetworkNotFoundException
from sybil_engine.data.networks import get_chain_instance_for_network
from test import init_set_test_config


class TestNetworks(unittest.TestCase):
    init_set_test_config()

    # def test_get_chain_instance_for_network(self):
    #     chain_instance = get_chain_instance_for_network('ZKSYNC', 'LOCAL')
    #
    #     self.assertEqual(chain_instance['chain'], 'ZKSYNC')
    #     self.assertEqual(chain_instance['gas_token'], 'ETH')
    #
    # def test_get_error_on_chain_instance_for_network(self):
    #     with self.assertRaises(NetworkNotFoundException):
    #         get_chain_instance_for_network('TEST', 'LOCAL')
