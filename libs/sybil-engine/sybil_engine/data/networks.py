import random
from typing import Dict, Any

from loguru import logger
from sybil_engine.data.tokens import get_tokens_for_chain

from sybil_engine.config.app_config import get_network, get_gas_prices
from sybil_engine.data.exception import NetworkNotFoundException
from sybil_engine.utils.file_loader import load_json_resource
from sybil_engine.utils.utils import ConfigurationException


NETWORK_FILES = {
    'MAIN': 'main/networks.json',
    'LOCAL': 'local/networks.json',
    'GOERLI': 'goerli/networks.json',
}


class NetworkManager:
    def __init__(self):
        self._chain_rpcs: Dict[str, str] = {}

    def get_ids_chain(self, network: str = None) -> Dict[int, str]:
        network = network or get_network()
        return {info["chain_id"]: chain for chain, info in self._get_chains(network).items()}

    def get_chain_instance_by_web3(self, web3, network: str = None):
        network = network or get_network()

        items = [item for item in self._get_chains(network).items() if item[1]["chain_id"] == web3.eth.chain_id]

        return self.get_chain_instance(items[0][0])

    def get_chain_instance(self, chain: str, network: str = None) -> Dict[str, Any]:
        network = network or get_network()
        all_chain_instances = self._get_chains(network)

        if chain not in all_chain_instances:
            raise NetworkNotFoundException(f"{chain} not found")

        chain_instance = all_chain_instances[chain].copy()
        self._configure_gas_prices(chain_instance, chain)
        self._configure_rpc(chain_instance, chain, network)
        chain_instance['chain'] = chain

        return chain_instance

    def get_supported_chains(self):
        return list(self._get_chains(get_network()).copy().keys())

    def _get_chains(self, network: str) -> Dict[str, Any]:
        if network not in NETWORK_FILES:
            raise NetworkNotFoundException(f"Network {network} not found")
        return load_json_resource(NETWORK_FILES[network])

    def _configure_gas_prices(self, chain_instance: Dict[str, Any], chain: str) -> None:
        gas_prices_gwei = get_gas_prices()
        chain_instance['l1_gas_price_gwei'] = gas_prices_gwei['ETH_MAINNET']

        if 'gas_price_gwei' not in chain_instance:
            if chain not in gas_prices_gwei:
                raise ConfigurationException(f"Gas price for {chain} not found in gas_price_gwei")
            chain_instance['gas_price_gwei'] = gas_prices_gwei[chain]

    def _configure_rpc(self, chain_instance: Dict[str, Any], chain: str, network: str) -> None:
        if chain not in self._chain_rpcs:
            self._set_rpc_for_chain(chain, network)
        chain_instance['rpc'] = self._chain_rpcs[chain]

    def _set_rpc_for_chain(self, chain: str, network: str) -> None:
        chain_config = self._get_chains(network)[chain]
        rpc_config = chain_config['rpc']

        if isinstance(rpc_config, list):
            available_rpcs = rpc_config.copy()
            if chain in self._chain_rpcs and len(available_rpcs) > 1:
                try:
                    available_rpcs.remove(self._chain_rpcs[chain])
                except ValueError:
                    pass

            self._chain_rpcs[chain] = random.choice(available_rpcs)
        else:
            self._chain_rpcs[chain] = rpc_config

        logger.info(f"{chain} rpc is set to {self._chain_rpcs[chain]}")


network_manager = NetworkManager()


def get_ids_chain():
    return network_manager.get_ids_chain()

def get_token_address(web3, token):
    return get_tokens_for_chain(get_chain_name_by_id(web3))[token]

def get_chain_name_by_id(web3):
    return get_ids_chain()[web3.eth.chain_id]

def get_chain_instance(chain: str):
    return network_manager.get_chain_instance(chain)

def get_chain_instance_for_network(chain: str, network: str):
    return network_manager.get_chain_instance(chain, network)

