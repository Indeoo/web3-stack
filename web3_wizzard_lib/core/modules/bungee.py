from typing import Union

import requests
from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance_utils import get_native_balance, interval_to_eth_balance, from_wei_to_eth
from sybil_engine.module.module import Module
from sybil_engine.utils.utils import ConfigurationException
from sybil_engine.utils.validation_utils import validate_chain, validate_refuel_interval
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.bungee import bungee_chain_ids, Bungee


class BungeeRefuel(Module):
    module_name = 'BUNGEE'
    module_config = 'bungee_config'

    def execute(self, refuel_amount_interval, from_chain, to_chain, account):
        from_chain_instance = get_chain_instance(from_chain)
        web3 = init_web3(from_chain_instance, account.proxy)

        bungee_contract = get_contracts_for_chain(from_chain)['BUNGEE']
        bungee = Bungee(bungee_contract, web3)

        try:
            limits = self.get_bungee_limits(from_chain)

            to_chain_limits = [
                chain for chain in limits if chain["chainId"] == bungee_chain_ids[to_chain] and chain["isEnabled"]
            ]

            if to_chain_limits:
                min_amount = float(from_wei_to_eth(int(to_chain_limits[0]["minAmount"])))
                max_amount = float(from_wei_to_eth(int(to_chain_limits[0]["maxAmount"])))

                if refuel_amount_interval == 'max':
                    refuel_amount_interval = {'from': max_amount * 0.9, 'to': max_amount * 0.98}

                if refuel_amount_interval == '':
                    refuel_amount_interval = {'from': min_amount, 'to': max_amount}

                if refuel_amount_interval['from'] < min_amount:
                    raise ConfigurationException(
                        f'Min refuel amount for {from_chain} is {min_amount} < {refuel_amount_interval["from"]}')

                if refuel_amount_interval['to'] > max_amount:
                    raise ConfigurationException(
                        f'Max refuel amount for {from_chain} is {max_amount} > {refuel_amount_interval["to"]}')

                native_without_min = get_native_balance(account, web3, from_chain_instance).minus(
                    self.min_native_balance)

                amount = interval_to_eth_balance(refuel_amount_interval, account, from_chain, web3)

                if amount.wei > native_without_min.wei:
                    amount = native_without_min

                logger.info(f"Refuel {from_chain.title()} > {to_chain.title()} | {amount}")

                bungee.refuel(account, to_chain, amount.wei)
            else:
                logger.info("skip")
        except Exception as e:
            logger.error(f"Bungee refuel error | error {e}")

    def get_bungee_limits(self, from_chain) -> Union[dict, bool]:
        bungee_data = self.get_bungee_data()

        try:
            if from_chain == 'ZKSYNC':
                limits = [chain_data for chain_data in bungee_data if chain_data["name"] == "zkSync"][0]["limits"]
            elif from_chain == 'ARBITRUM':
                limits = [chain_data for chain_data in bungee_data if chain_data["name"] == "Arbitrum"][0]["limits"]
            elif from_chain == 'OPTIMISM':
                limits = [chain_data for chain_data in bungee_data if chain_data["name"] == "Optimism"][0]["limits"]
            elif from_chain == 'POLYGON':
                limits = [chain_data for chain_data in bungee_data if chain_data["name"] == "Polygon"][0]["limits"]
            elif from_chain == 'AVALANCHE':
                limits = [chain_data for chain_data in bungee_data if chain_data["name"] == "Avalanche"][0]["limits"]
            elif from_chain == 'BSC':
                limits = [chain_data for chain_data in bungee_data if chain_data["name"] == "BSC"][0]["limits"]
            elif from_chain == 'BASE':
                limits = [chain_data for chain_data in bungee_data if chain_data["name"] == "Base"][0]["limits"]
            else:
                raise Exception("Not supported")

            return limits
        except Exception as e:
            return False

    def get_bungee_data(self):
        url = "https://refuel.socket.tech/chains"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()["result"]
            return data
        return False

    def log(self):
        return "BUNGEE REFUEL"

    def parse_params(self, module_params):
        validate_chain(module_params['from_chain'])
        validate_chain(module_params['to_chain'])
        validate_refuel_interval(module_params['refuel_amount_interval'])

        return module_params['refuel_amount_interval'], module_params['from_chain'], module_params['to_chain']
