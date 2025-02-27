import requests
from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.module.module import Module
from web3 import Web3

from web3_wizzard_lib.core.utils.statistic_utils import get_statistic_writer, statistic_date_string


class AirdropPrinter(Module):
    module_name = 'AIRDROP_PRINTER'
    module_config = None

    claimers = {
        "L0": "0xB09F16F625B363875e39ADa56C03682088471523",
        "SCROLL": "0xE8bE8eB940c0ca3BD19D911CD3bEBc97Bea0ED62",
        "ZKSYNC": "0x66Fd4FC8FA52c9bec2AbA368047A0b27e24ecfe4",
        "ORBITER": "0x13dFDd3a9B39323F228Daf73B62C23F7017E4679",
        "ODOS": "0x4C8f8055D88705f52c9994969DDe61AB574895a3"
    }

    EMPTY_ADDRESS = '-'

    chains = ["ARBITRUM", "ZKSYNC", "SCROLL", "BASE"]

    def execute(self, account, statistic_write='GOOGLE'):
        chain_contracts = {}
        for chain in self.chains:
            chain_instance = get_chain_instance(chain)

            datas = self.find_interacted_contracts_hash(
                account.address,
                chain_instance['api_scan'],
                chain_instance['api_scan_key']
            )

            chain_contracts[chain] = datas['result']

        account_links = {}

        for project, claim_address in self.claimers.items():
            for chain, datas in chain_contracts.items():
                chain_instance = get_chain_instance(chain)
                for data in datas:
                    if data['to'] != "" and claim_address == Web3.to_checksum_address(data['to']):
                        account_links[project] = chain_instance['scan'] + "tx/" + data['hash']

            if account_links.get(project) is None:
                account_links[project] = self.EMPTY_ADDRESS

        logger.info(account_links)
        statistics_writer = get_statistic_writer()
        job_name = f"airdrops_{statistic_date_string}"
        statistics_writer.init_if_required(job_name, ['#', 'Address'] + list(self.claimers.keys()))

        value_row = [account.app_id, account.address]
        for project, address in account_links.items():
            value_row.append(address)

        statistics_writer.write_row(job_name, value_row)

    def find_interacted_contracts_hash(self, wallet_address, api_url, api_key):
        api_url = f"{api_url}/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=latest&sort=asc&apikey={api_key}&offset=200"

        if "base" in api_url:
            logger.info(f"BASE {api_url}")
            pass

        response = requests.get(api_url)
        data = response.json()

        if data['status'] == '1' and data['message'] == 'OK':
            return data
        else:
            logger.info("nothing")
            logger.info(data)
            pass
            return data

    def log(self):
        return "AIRDROP PRINTER"
