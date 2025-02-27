import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from loguru import logger
from sybil_engine.contract.send import Send
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.utils.web3_utils import init_web3
from web3_wizzard_lib.core.utils.sub_module import SubModule


class OrbiterClaim(SubModule):
    module_name = 'ORBITER_CLAIM'

    nft_address = "0x13dFDd3a9B39323F228Daf73B62C23F7017E4679"

    def execute(self, account, chain='ARBITRUM'):

        # message to sign Orbiter Airdrop
        message_text = "Orbiter Airdrop"
        text_hex = "0x" + message_text.encode('utf-8').hex()
        text_encoded = encode_defunct(hexstr=text_hex)
        signed_message = Account.sign_message(text_encoded, private_key=account.key)

        signature = f'0x{signed_message.signature.hex()}'
        headers = {
            "token": signature
        }

        result = requests.post(
            "https://airdrop-api.orbiter.finance/airdrop/snapshot",
            headers=headers
        ).json()

        chain_id = result['result']['chainId']

        chain, data = self.form_data(chain, chain_id, result)

        try:
            self.send_transaction(account, chain, data)
        except Exception as e:
            self.send_transaction(account, chain, data.replace("0000000000000000014", "0000000000000000013"))

    def form_data(self, chain, chain_id, result):
        amount_str = result['result']['proof'][0]['amount']
        logger.info(f"Orbiter Airdrop snapshot result: {amount_str}")
        amount_int = int(amount_str.replace(".", ""))
        logger.info(f"AMOUNT INT: {amount_int}")
        hex_value = hex(amount_int)[2:]
        logger.info(f"AMOUNT: {hex_value}")
        logger.info(f"HEX {hex_value}")
        if int(chain_id) == 42161:
            chain = 'ARBITRUM'
            data = "0xfa5c4e99071cbb2ff029ddaf4b691745b2ba185cbe9ca2f5fa9e7358bada8fbdce764291"
            data += f"0000000000000000000000000000000000000000000000{hex_value}00000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000014"
        else:
            data = "0xfa5c4e995d32ba2a988b8fa6c2ae96d3b5980c67e8d8cfbf0d4c89479b79c1e277843438"
            data += f"000000000000000000000000000000000000000000000010b202b565eb37160000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000010"
            chain = 'BASE'
        for line_data in result['result']['proof'][0]['data']:
            data += line_data[2:]
        logger.info(data)
        return chain, data

    def send_transaction(self, account, chain, data):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)
        Send(None, web3).send_to_wallet(
            account,
            self.nft_address,
            NativeBalance(0, chain, "ETH"),
            data
        )

    def log(self):
        return "ORBITER NFT"

def round_to_custom_precision(number, precision):
    # Find the rounding factor (10^precision)
    factor = 10 ** precision
    # Perform rounding
    return round(number / factor) * factor


def truncate_to_decimal_places(value, decimals):
    factor = 10 ** decimals
    return int(float(int(value * factor)) / factor)