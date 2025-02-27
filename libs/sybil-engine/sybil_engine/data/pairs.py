import random
from collections import defaultdict

from sybil_engine.config.app_config import get_network
from sybil_engine.data.exception import NetworkNotFoundException
from sybil_engine.utils.file_loader import load_json_resource
from sybil_engine.utils.utils import ConfigurationException


class Pairs:
    def __init__(self, swap_facade):
        self.swap_facade = swap_facade

    def get_warmup_pair_swaps(self, allowed_swaps, chain, pair_names, warmup_amount, warm_token):
        return random.choices(self.get_all_pair_swaps(chain, pair_names, warm_token, allowed_swaps), k=warmup_amount)

    def get_all_pair_swaps(self, chain, pair_names, warm_token, allowed_swaps=None):
        if allowed_swaps is not None:
            swap_apps = set(self.swap_facade.get_swap_apps_by_chain(chain)) & set(allowed_swaps)
        else:
            swap_apps = self.swap_facade.get_swap_apps_by_chain(chain)

        pairs = [
            pair for pair in _get_pairs_by_swap_apps(swap_apps, chain)
            if pair['tokens'][0] == warm_token and (not pair_names or pair['name'] in pair_names)
        ]
        if not pairs:
            raise ConfigurationException(f"Wrong pairs {pair_names}")
        grouped_pairs = defaultdict(list, {item['name']: [] for item in pairs})
        for item in pairs:
            grouped_pairs[item['name']].append(item)

        all_pair_swaps = [
            ({**{k: v for d in group for k, v in d.items()}, 'app': [item['app'] for item in group]},
             [item['app'] for item in group])
            for group in grouped_pairs.values()
        ]
        return all_pair_swaps

    def get_pair_names(self, chain, receive_token):
        return list(set([pair_name['name'] for pair_name in self.get_all_pairs_for_chain(receive_token, chain)]))

    def get_pairs_by_tokens(self, from_token, to_token, chain, swap_apps=None):
        return _get_pairs_by_swap_apps(
            swap_apps or self.swap_facade.get_swap_apps_by_chain(chain), chain,
            pairs_list=[{from_token, to_token}]
        )

    def get_swap_apps_by_pair(self, from_token, to_token, chain):
        pairs = self.get_pairs_by_tokens(from_token, to_token, chain)

        return set([pair['app'] for pair in pairs])

    def get_all_pairs_for_chain(self, receive_token, chain):
        return [
            pair for pair in _get_pairs_by_swap_apps(self.swap_facade.get_swap_apps_by_chain(chain), chain)
            if pair['tokens'][0] == receive_token
        ]


def _get_swap_configuration_for_chain(chain):
    network = get_network()
    config_file = {
        'MAIN': 'main/pairs.json',
        'LOCAL': 'local/pairs.json',
        'GOERLI': 'goerli/pairs.json'
    }.get(network)

    if not config_file:
        raise NetworkNotFoundException(f"{chain} not found")

    return load_json_resource(config_file)[chain]


def _get_pairs_by_swap_apps(swap_apps, chain, pairs_list=None):
    pairs_from_config = _get_swap_configuration_for_chain(chain)
    return [
        {**pair, 'app': swap_name}
        for swap_name, pairs in pairs_from_config.items()
        if swap_name in swap_apps
        for pair in pairs
        if not pairs_list or set(pair['tokens']) in pairs_list
    ]
