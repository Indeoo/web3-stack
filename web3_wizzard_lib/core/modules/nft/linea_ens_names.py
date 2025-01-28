from random import choices
from string import ascii_letters, digits

import requests
from eth_utils import keccak
from faker import Faker
from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.retry import retry
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.linea_ens_names_contract import LineaEnsNamesContract
from web3_wizzard_lib.core.utils.sub_module import SubModule
from web3_wizzard_lib.core.modules.nft_minter import SkipRetryException


class LineaENSNames(SubModule):
    module_name = 'LINEA_ENS'
    nft_address = '0xDb75Db974B1F2bD3b5916d503036208064D18295'

    def execute(self, account: AppAccount, chain='LINEA'):
        self.sleep_after_conf = True

        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract = LineaEnsNamesContract(self.nft_address, web3)

        linea_name = self.get_available_name(contract)

        if contract.redeemed(account):
            #logger.info("[+] Web3 | Wallet already redeemed Linea name.")
            raise SkipRetryException("[+] Web3 | Wallet already redeemed Linea name.")

        logger.info(f"Minting {linea_name}.linea.eth for {account.address}")
        duration = 60 * 60 * 24 * 365 * 3  # 3 years
        secret, data = self.commit(account, linea_name, duration, contract)

        # Uncomment the following line to perform the registration
        self.register_poh(account, contract, data, duration, linea_name, secret)

    def get_available_name(self, contract):
        while True:
            linea_name = self.generate_linea_name()
            if contract.available(linea_name):
                break
            logger.warning(f'[-] Web3 | Linea name "{linea_name}.linea.eth" is unavailable. Retrying...')
        return linea_name

    @retry(max_attempts=20, retry_interval={'from': 10, 'to': 20})
    def register_poh(self, account, contract, data, duration, linea_name, secret):
        contract.register_poh(account, linea_name, duration, secret, data, self.get_poh_signature(account))

    def generate_linea_name(self):
        return Faker().user_name().replace('_', '-')

    def log(self):
        return "LINEA ENS"

    def commit(self, account, linea_name: str, duration: int, linea_ens_contract):
        secret = "0x" + ''.join(choices(ascii_letters + digits, k=10)).encode().hex().ljust(64, '0')
        hashed_name = self.namehash(f"{linea_name}.linea.eth")
        data = linea_ens_contract.addr_contract.functions.setAddr(
            hashed_name, 60,
            account.address
        )._encode_transaction_data()

        commitment = linea_ens_contract.make_commitment(
            account,
            linea_name,
            duration,
            secret,
            data,
        )

        linea_ens_contract.commit(account, commitment)

        return secret, data

    def namehash(self, name: str):
        labels = name.split('.')
        labels.reverse()
        result = "0000000000000000000000000000000000000000000000000000000000000000"

        for label in labels:
            hashed = keccak(text=label).hex()
            result = keccak(hexstr=result + hashed).hex()

        return "0x" + result

    def sleep_after_conf(self):
        return self.sleep_after_conf

    def get_poh_signature(self, account):
        headers = {
            "Origin": "https://relay.link",
            "Referer": "https://relay.link/"
        }

        r = requests.get(f'https://linea-poh-signer-api.linea.build/poh/{account.address}', headers=headers)
        if len(r.text) == 132 and r.text.startswith("0x"):
            return {"sign": r.text, "success": True, "msg": ""}
        elif "address not POH" in r.text:
            return {"sign": "", "success": False, "msg": "This wallet dont have POH"}
        else:
            raise Exception(r.text)
