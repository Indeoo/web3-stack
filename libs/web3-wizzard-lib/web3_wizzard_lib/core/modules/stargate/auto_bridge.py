import random

from loguru import logger
from sybil_engine.domain.balance.balance_utils import find_chain_with_max_usdc, find_chain_with_max_native
from sybil_engine.module.module import Module
from sybil_engine.utils.utils import randomized_sleeping
from sybil_engine.utils.web3_utils import print_account_data, get_all_account_data

from web3_wizzard_lib.core.modules.stargate.bridge import StargateBridge


class StargateAutoBridge(Module):
    module_name = 'STARGATE_AUTO_BRIDGE'
    module_config = 'stargate_auto_bridge_config'

    def execute(self, bridge_amount_interval, token, original_chain_sequence, sleep_interval, retry_interval,
                end_network, only_end_network_bridge, account):
        chain_sequence = original_chain_sequence.copy()

        logger.info(f"=============== Bridging for {account.address} ===============")

        account_data = get_all_account_data(account, chain_sequence)
        print_account_data(account_data)

        if token == 'USDC':
            max_usdc_chain, usdc, native_balance, web3 = find_chain_with_max_usdc(account_data)
        else:
            max_usdc_chain, usdc, native_balance, web3 = find_chain_with_max_native(account_data)

        logger.info(f"Chain with biggest {token} balance is {max_usdc_chain}")

        if only_end_network_bridge:
            if end_network == '':
                raise Exception("Env network should be declared on ONLY_END_NETWORK_BRIDGE=True")
            shuffled_chain_sequence = [max_usdc_chain] + [end_network]
        else:
            shuffled_chain_sequence = self.shuffle_chain_sequence(chain_sequence, max_usdc_chain, end_network)

        chain_sequence_readable = 'Result chain sequence: ' + ' -> '.join(shuffled_chain_sequence)
        logger.info(chain_sequence_readable)
        self.process_bridge(bridge_amount_interval, token, account, retry_interval, shuffled_chain_sequence,
                            sleep_interval)

    def process_bridge(self, bridge_amount_interval, bridge_token, account, retry_interval, shuffled_chain_sequence,
                       sleep_interval):
        for chain_number, _ in enumerate(shuffled_chain_sequence[:-1]):
            from_chain = shuffled_chain_sequence[chain_number]
            to_chain = shuffled_chain_sequence[chain_number + 1]

            StargateBridge(retry_interval).bridge(
                self.min_native_balance,
                account,
                bridge_amount_interval,
                bridge_token,
                from_chain,
                to_chain
            )
            randomized_sleeping(sleep_interval)

    def shuffle_chain_sequence(self, chain_sequence, max_usdc_chain, end_network):
        chain_sequence.remove(max_usdc_chain)

        while True:
            random.shuffle(chain_sequence)

            # If reshuffle doesn't result in the prohibited sequence, break out of the loop
            if not any((chain_sequence[i] == 'FANTOM' and chain_sequence[i + 1] == 'BASE') or
                       (chain_sequence[i] == 'BASE' and chain_sequence[i + 1] == 'FANTOM') or
                       (max_usdc_chain == 'FANTOM' and chain_sequence[0] == 'BASE') or
                       (max_usdc_chain == 'BASE' and chain_sequence[0] == 'FANTOM')
                       for i in range(len(chain_sequence) - 1)):
                break

        if end_network and chain_sequence[-1] != end_network:
            chain_sequence.append(end_network)

        return [max_usdc_chain] + chain_sequence

    def log(self):
        return "STARGATE AUTO"

    def parse_params(self, module_params):
        return (
            module_params['bridge_amount_interval'],
            module_params['bridge_token'],
            module_params['original_chain_sequence'],
            module_params['sleep_interval'],
            module_params['retry_interval'],
            module_params['end_network'],
            module_params['only_end_network_bridge']
        )
