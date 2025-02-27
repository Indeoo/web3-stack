import requests
from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaCultureWeek4Day1(NftSubmodule):
    module_name = 'LINEA_CULTURE_4_1'
    nft_address = '0xAd626D0F8BE64076C4c27a583e3df3878874467E'

    def execute(self, account: AppAccount, chain='LINEA', wei_cost=from_eth_to_wei(0)):
        url = 'https://public-api.phosphor.xyz/v1/purchase-intents'

        data = {
            "buyer": {
                "eth_address": account.address
            },
            "listing_id": "fceb2be9-f9fd-458a-8952-9a0a6f873aff",
            "provider": "MINT_VOUCHER",
            "quantity": 1
        }

        proxy = {
            'http': account.proxy,
            'https': account.proxy
        }

        response = requests.post(url, json=data, proxies=proxy)

        signature = response.json()['data']['signature'][2:]
        expiry = response.json()['data']['voucher']['expiry']

        data = f"0xd4dfd6bc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000{decimal_to_hex(expiry)}00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000041{signature}00000000000000000000000000000000000000000000000000000000000000"

        Send(
            None,
            self.create_web3(account, chain)
        ).send_to_wallet(
            account,
            self.nft_address,
            NativeBalance(wei_cost, chain, "ETH"),
            data
        )

    def log(self):
        return "LINEA CULTURE 4 WEEK DAY 1 (Coop Records)"

def decimal_to_hex(decimal):
    if decimal == 0:
        return "0x0"
    hex_digits = "0123456789ABCDEF"
    hex_result = ""
    while decimal > 0:
        remainder = decimal % 16
        hex_result = hex_digits[remainder] + hex_result
        decimal = decimal // 16
    return hex_result.lower()