import requests

from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaWheel(NftSubmodule):
    module_name = 'LINEA_WHEEL'
    nft_address = '0xDb3a3929269281F157A58D91289185F21E30A1e0'

    def execute(self, account, chain='LINEA'):
        web3 = self.create_web3(account, chain)
        data = create_data(get_jwt_token(account, web3, self.nft_address))

        Send(
            None,
            self.create_web3(account, chain)
        ).send_to_wallet(
            account,
            self.nft_address,
            NativeBalance(0, chain, "ETH"),
            data
        )

    def log(self):
        return "LINEA WHEEL"

def create_data(jwt_token):
    pass


def get_jwt_token(account, web3, contract_address):
    nonce = requests.get("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/nonce")
    print(nonce.text)
    nonce_text = nonce.text

    message = f'{"domain":"linea.build","address":"0x6903d837A3CE9567F56067341f73EBF65A1746Db","statement":"Welcome to Linea Hub. Signing is the only way we can truly know that you are the owner of the wallet you are connecting. Signing is a safe, gas-less transaction that does not in any way give Linea Hub permission to perform any transactions with your wallet.","uri":"https://linea.build/hub/rewards","version":"1","chainId":1,"nonce":{nonce_text},"issuedAt":"2025-08-08T09:22:47.537Z","requestId":"ae98b9b4-daaf-4bb3-b5e0-3f07175906ed"}'
    signed_message = web3.eth.account.sign_message(message, private_key=account.key)

    params = {
        "signedMessage": signed_message,
        "messageToSign": message,
        "publicWalletAddress": "0x6903d837A3CE9567F56067341f73EBF65A1746Db", "chain": "EVM", "walletName": "metamask",
        "walletProvider": "browserExtension", "network": "59144", "additionalWalletAddresses": [],
        "sessionPublicKey": "02fe8547be43b4baa7b22169fa7d33b72f17f1bc4eef8e0358321a34026f562c61"
    }

    requests.post("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/verify", params)
#
# if __name__ == '__main__':
#     nonce = requests.get("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/nonce")
#     print(nonce.text)
#     nonce_text = nonce.text
#
#     message = f'{"domain":"linea.build","address":"0x6903d837A3CE9567F56067341f73EBF65A1746Db","statement":"Welcome to Linea Hub. Signing is the only way we can truly know that you are the owner of the wallet you are connecting. Signing is a safe, gas-less transaction that does not in any way give Linea Hub permission to perform any transactions with your wallet.","uri":"https://linea.build/hub/rewards","version":"1","chainId":1,"nonce":{nonce_text},"issuedAt":"2025-08-08T09:22:47.537Z","requestId":"ae98b9b4-daaf-4bb3-b5e0-3f07175906ed"}'
#     signed_message = web3.eth.account.sign_message(encoded_message, private_key=account.key )
#
#     params = {
#         "signedMessage": "0x10f63acf56ced627247230221472a0b3244407a8690c71df24b3771bb82d28d92c9c9489bb37d78645ac17ee4548b2f0e5bba2a60e5aa07fee980d9ab79cac461b",
#         "messageToSign": message,
#         "publicWalletAddress": "0x6903d837A3CE9567F56067341f73EBF65A1746Db", "chain": "EVM", "walletName": "metamask",
#         "walletProvider": "browserExtension", "network": "59144", "additionalWalletAddresses": [],
#         "sessionPublicKey": "02fe8547be43b4baa7b22169fa7d33b72f17f1bc4eef8e0358321a34026f562c61"
#     }
#
#     requests.post("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/verify")