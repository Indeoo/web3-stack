import requests
from eth_account.messages import encode_defunct

from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaWheel(NftSubmodule):
    module_name = 'LINEA_WHEEL'
    nft_address = '0xDb3a3929269281F157A58D91289185F21E30A1e0'

    def execute(self, account, chain='LINEA'):
        web3 = init_web3(
            {
                "rpc": "https://rpc.linea.build",
                "poa": "true"
            },
            account.proxy
        )
        jwt_token = get_jwt_token(account, web3, self.nft_address)
        data = create_data(jwt_token)

        # Send(
        #     None,
        #     self.create_web3(account, chain)
        # ).send_to_wallet(
        #     account,
        #     self.nft_address,
        #     NativeBalance(0, chain, "ETH"),
        #     data
        # )

    def log(self):
        return "LINEA WHEEL"

def get_jwt_token(account, web3, contract_address):
    nonce = requests.get("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/nonce")
    print(f"NONCE {nonce.text}")
    nonce_text = nonce.json()['nonce']

    message_to_sign = f"linea.build wants you to sign in with your Ethereum account:\n{account.address}\n\nWelcome to Linea Hub. Signing is the only way we can truly know that you are the owner of the wallet you are connecting. Signing is a safe, gas-less transaction that does not in any way give Linea Hub permission to perform any transactions with your wallet.\n\nURI: https://linea.build/hub/rewards\nVersion: 1\nChain ID: 59144\nNonce: {nonce_text}\nIssued At: 2025-08-08T13:08:56.275Z\nRequest ID: ae98b9b4-daaf-4bb3-b5e0-3f07175906ed"
    print(f"message to sign: {message_to_sign}")
    encoded_message_to_sign = encode_defunct(text=message_to_sign)
    signed_message = web3.eth.account.sign_message(encoded_message_to_sign, private_key=account.key)

    print(f"HASH {signed_message.signature.hex()}")

    params = {
        "signedMessage": signed_message.signature.hex(),
        "messageToSign": message_to_sign,
        "publicWalletAddress": account.address, "chain": "EVM", "walletName": "metamask",
        "walletProvider": "browserExtension", "network": "59144", "additionalWalletAddresses": [],
        "sessionPublicKey": "03225f269ac4021962998f67e5486b8cc9bcdc3936542a0fb69fdb128c92c299f9"
    }

    result = requests.post("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/verify",
                           json=params)

    print(result)
    print(result.text)

    return result.text

def create_data(jwt_token):
    # Do not implement yet
    pass