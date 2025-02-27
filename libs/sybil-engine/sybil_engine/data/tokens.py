from sybil_engine.config.app_config import get_network
from sybil_engine.data.exception import NetworkNotFoundException
from sybil_engine.utils.file_loader import load_json_resource


def get_tokens_for_chain(chain):
    network = get_network()

    if network == 'MAIN':
        return load_json_resource("main/tokens.json")[chain]
    elif network == 'LOCAL':
        return load_json_resource("local/tokens.json")[chain]
    elif network == 'GOERLI':
        return load_json_resource("goerli/tokens.json")[chain]
    else:
        raise NetworkNotFoundException(f"{chain} not found")
