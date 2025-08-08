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


def create_data(jwt_token):
    import time
    from sybil_engine.utils.file_loader import load_abi

    # Load contract ABI and create contract instance
    abi = load_abi("resources/abi/linea_wheel/spin.json")
    # We need to use a web3 instance, but since we don't have access to it here,
    # we'll create a simple encoded call

    # Extract signature from JWT token if available
    # For now, use placeholder values since we don't know the JWT structure
    nonce_param = int(time.time())
    expiration_timestamp = int(time.time()) + 3600
    boost = 100000000  # 1.0x boost (BASE_POINT = 1e8)

    # Placeholder signature - this would need to be extracted from JWT or signed properly
    signature = (
        b'\x00' * 32,  # r
        b'\x00' * 32,  # s
        27  # v
    )

    # Return the function signature and encoded parameters
    # participate(uint64,uint256,uint64,(bytes32,bytes32,uint8))
    from web3 import Web3

    # Create function signature hash
    function_signature = Web3.keccak(text="participate(uint64,uint256,uint64,(bytes32,bytes32,uint8))")[:4]

    # Encode parameters (simplified - in production would use proper ABI encoding)
    encoded_params = Web3.solidity_keccak(
        ['uint64', 'uint256', 'uint64', 'bytes32', 'bytes32', 'uint8'],
        [nonce_param, expiration_timestamp, boost, signature[0], signature[1], signature[2]]
    )

    return function_signature + encoded_params[:60]  # Truncate to reasonable length


def get_jwt_token(account, web3, contract_address):
    nonce = requests.get("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/nonce")
    print(f"NONCE {nonce.text}")
    nonce_text = nonce.text

    message_to_sign = f"linea.build wants you to sign in with your Ethereum account:\n{account.address}\n\nWelcome to Linea Hub. Signing is the only way we can truly know that you are the owner of the wallet you are connecting. Signing is a safe, gas-less transaction that does not in any way give Linea Hub permission to perform any transactions with your wallet.\n\nURI: https://linea.build/hub/rewards\nVersion: 1\nChain ID: 59144\nNonce: {nonce_text}\nIssued At: 2025-08-08T09:33:52.424Z\nRequest ID: ae98b9b4-daaf-4bb3-b5e0-3f07175906ed"
    encoded_message_to_sign = encode_defunct(text=message_to_sign)
    signed_message = web3.eth.account.sign_message(encoded_message_to_sign, private_key=account.key)

    print(f"HASH {signed_message.signature.hex()}")

    params = {
        "signedMessage": signed_message.signature.hex(),
        "messageToSign": message_to_sign,
        "publicWalletAddress": account.address, "chain": "EVM", "walletName": "metamask",
        "walletProvider": "browserExtension", "network": "59144", "additionalWalletAddresses": [],
        "sessionPublicKey": "02fe8547be43b4baa7b22169fa7d33b72f17f1bc4eef8e0358321a34026f562c61"
    }

    result = requests.post("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/verify",
                           json=params)

    print(result)
    print(result.text)

    return result.text
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
