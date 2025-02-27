import random

from loguru import logger

from sybil_engine.config.app_config import get_network, get_gas_prices
from sybil_engine.data.exception import NetworkNotFoundException
from sybil_engine.utils.file_loader import load_json_resource
from sybil_engine.utils.utils import ConfigurationException

chain_rpcs = {}


def get_ids_chain():
    return {info["chain_id"]: chain for chain, info in get_networks(get_network()).items()}


def get_chain_instance(chain: str):
    return get_chain_instance_for_network(chain, get_network())


def get_chain_instance_for_network(chain: str, network: str):
    networks = get_networks(network).copy()

    if chain not in networks:
        raise NetworkNotFoundException(f"{chain} not found")

    chain_instance = networks[chain]

    gas_prices_gwei = get_gas_prices()
    chain_instance['l1_gas_price_gwei'] = gas_prices_gwei['ETH_MAINNET']
    if 'gas_price_gwei' not in chain_instance:
        if chain not in gas_prices_gwei:
            raise ConfigurationException(f"Gas price for {chain} not found in gas_price_gwei")
        chain_instance['gas_price_gwei'] = gas_prices_gwei[chain]

    chain_instance['chain'] = chain

    if chain not in list(chain_rpcs.keys()):
        set_rpc_for_chain(chain)

    chain_instance['rpc'] = chain_rpcs[chain]

    return chain_instance


def set_rpc_for_chain(chain):
    network = get_networks(get_network()).copy()[chain]

    if isinstance(network['rpc'], list):
        if len(network['rpc']) > 1 and chain in list(chain_rpcs.keys()):
            network['rpc'].remove(chain_rpcs[chain])

        chain_rpcs[chain] = random.choice(network['rpc'])
    else:
        chain_rpcs[chain] = network['rpc']

    logger.info(f"{chain} rpc is set to {chain_rpcs[chain]}")


def get_networks(network):
    if network == 'MAIN':
        return load_json_resource("main/networks.json")
    elif network == 'LOCAL':
        return load_json_resource("local/networks.json")
    elif network == 'GOERLI':
        return load_json_resource("goerli/networks.json")
    else:
        raise NetworkNotFoundException(f"Network {network} not found")
