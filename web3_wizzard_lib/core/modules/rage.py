import requests
from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import Erc20Balance
from sybil_engine.module.module import Module
from sybil_engine.utils.accumulator import add_accumulator_balance
from sybil_engine.utils.utils import AccountException
from sybil_engine.utils.web3_utils import init_web3
from web3 import Web3

from web3_wizzard_lib.core.contract.rage_claim import RageClaimer


class Rage(Module):
    module_name = 'RAGE_WITHDRAW'
    module_config = None

    def execute(self, account, chain='ARBITRUM'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain_instance['chain'])['RAGE_CLAIM']
        rage = RageClaimer(contract_address, web3)

        amount, index, merkle_proof = self.get_data(account)
        usdc_amount = int(amount, 16)

        usdc = Erc20Balance(usdc_amount, chain, 'USDC')

        logger.info(f"Withdraw {usdc.log_line()}")

        bytes32_array = [Web3.to_bytes(hexstr=hex_string[2:]) for hex_string in merkle_proof]

        rage.claim(account, usdc_amount, index, bytes32_array)
        add_accumulator_balance("Total rage withdraw", usdc_amount)

    def get_data(self, account):
        # Make the GET request
        url = f"https://www.app.rage.trade/api/merkel-proof?address={account.address}"

        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            claim_data = response.json()["claim"]

            return claim_data["amount"], claim_data["index"], claim_data["proof"]
        else:
            raise AccountException(f"HTTP request failed with status code {response.status_code}")

    def log(self):
        return "RAGE CLAIMER"
