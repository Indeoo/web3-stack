import requests
from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.utils import AppException

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaCultureWeek4Day2(NftSubmodule):
    module_name = 'LINEA_CULTURE_4_4'
    nft_address = '0x3EB78e881b28B71329344dF622Ea3A682538EC6a'

    def execute(self, account: AppAccount, chain='LINEA', wei_cost=from_eth_to_wei(0)):
        url = 'https://public-api.phosphor.xyz/v1/purchase-intents'

        data = {
            "buyer": {
                "eth_address": account.address
            },
            "listing_id": "d3542d49-273c-4f2d-9d33-8904c773ed14",
            "provider": "MINT_VOUCHER",
            "quantity": 1
        }

        proxy = {
            'http': account.proxy,
            'https': account.proxy
        }

        response = requests.post(url, json=data, proxies=proxy)

        if 'error' in response.json():
            raise AppException(response.json())

        signature = response.json()['data']['signature'][2:]
        expiry = response.json()['data']['voucher']['expiry']
        nonce = response.json()['data']['voucher']['nonce']
        tokenID = response.json()['data']['voucher']['token_id']

        data = f"0xd4dfd6bc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000{nonce}00000000000000000000000000000000000000000000000000000000{decimal_to_hex(expiry)}0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000{tokenID}000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000041{signature}00000000000000000000000000000000000000000000000000000000000000"

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
        return "LINEA CULTURE 4 WEEK DAY 4 (Fruit Crux)"


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
