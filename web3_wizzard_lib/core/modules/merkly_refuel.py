import random

from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance_utils import interval_to_eth_balance, verify_balance, from_wei_to_eth
from sybil_engine.module.module import Module
from sybil_engine.utils.utils import ConfigurationException, randomized_sleeping, print_exception_chain
from sybil_engine.utils.validation_utils import validate_chain, validate_refuel_interval
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.merkly_minter import MerklyMinter
from web3_wizzard_lib.core.modules.stargate.l0_data import l0_chain_ids


class MerklyRefuel(Module):
    module_name = 'MERKLY_REFUEL'
    module_config = 'merkly_refuel_config'

    def execute(self, start_chain, end_chain, chains, refuel_amount_interval, sleeping_interval, account):
        from_chain_instance = get_chain_instance(start_chain)
        web3 = init_web3(from_chain_instance, account.proxy)

        if start_chain not in chains or end_chain not in chains:
            raise ConfigurationException(f"'end_chain' and 'start_start' should be in 'chains'. Actual:"
                                         f"start_chain: {start_chain} end_chain: {end_chain} chains: {chains}"
                                         )

        merkly_contract = get_contracts_for_chain(start_chain)['MERKLY']
        merkly = MerklyMinter(merkly_contract, web3)

        self.shuffle_chain_sequence(start_chain, end_chain, chains)

        logger.info(f"Refuel chain sequence: {chains}")

        for current_chain, next_chain in zip(chains, chains[1:]):
            native_without_min = verify_balance(self.min_native_balance, from_chain_instance, account, web3)

            amount = interval_to_eth_balance(refuel_amount_interval, account, start_chain, web3)

            if amount.wei > native_without_min.wei:
                amount = native_without_min

            logger.info(f"Refuel {current_chain} > {next_chain} | {amount}")

            hex_amount = merkly.decimal_to_hex_padded(amount.wei)

            try:
                fee = merkly.estimate_send_fee(account, l0_chain_ids[next_chain], hex_amount)
                logger.info(f"L0 Fee: {from_wei_to_eth(fee)} ETH")

                merkly.refuel(account, l0_chain_ids[next_chain], amount.wei, fee)
                randomized_sleeping(sleeping_interval)
            except Exception as e:
                print_exception_chain(e)

    def shuffle_chain_sequence(self, start_chain, end_chain, chain_sequence):
        if start_chain != '':
            chain_sequence.remove(start_chain)

        if end_chain != '' and end_chain in chain_sequence:
            chain_sequence.remove(end_chain)

        random.shuffle(chain_sequence)

        if start_chain != '':
            chain_sequence.insert(0, start_chain)

        if end_chain != '':
            chain_sequence.append(end_chain)

        return chain_sequence

    def log(self):
        return "MERKLY REFUEL"

    def parse_params(self, module_params):
        validate_chain(module_params['end_chain'])
        validate_refuel_interval(module_params['refuel_amount_interval'])

        return (
            module_params['start_chain'],
            module_params['end_chain'],
            module_params['chains'],
            module_params['refuel_amount_interval'],
            module_params['sleeping_interval']
        )
