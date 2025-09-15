import os
import time
import uuid

import requests
from eth_account.messages import encode_defunct
from web3 import Web3
from datetime import datetime, timezone

from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule

# 1. Connect
# 2. Verify
# 3. Spin
class LineaWheel(NftSubmodule):
    abi = '[{"inputs":[{"internalType":"address","name":"_trustedForwarderAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"AccessControlBadConfirmation","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"bytes32","name":"neededRole","type":"bytes32"}],"name":"AccessControlUnauthorizedAccount","type":"error"},{"inputs":[],"name":"AddressZero","type":"error"},{"inputs":[],"name":"ECDSAInvalidSignature","type":"error"},{"inputs":[{"internalType":"uint256","name":"length","type":"uint256"}],"name":"ECDSAInvalidSignatureLength","type":"error"},{"inputs":[{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"ECDSAInvalidSignatureS","type":"error"},{"inputs":[],"name":"ERC20PrizeWrongParam","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"InvalidLotAmount","type":"error"},{"inputs":[{"internalType":"address","name":"prizeAddress","type":"address"}],"name":"InvalidPrize","type":"error"},{"inputs":[{"internalType":"uint256","name":"requestId","type":"uint256"}],"name":"InvalidRequestId","type":"error"},{"inputs":[{"internalType":"uint256","name":"totalProbabilities","type":"uint256"}],"name":"MaxProbabilityExceeded","type":"error"},{"inputs":[{"internalType":"uint256","name":"lotAmount","type":"uint256"},{"internalType":"uint256","name":"erc721PrizeAmount","type":"uint256"}],"name":"MismatchERC721PrizeAmount","type":"error"},{"inputs":[],"name":"NativeTokenTransferFailed","type":"error"},{"inputs":[{"internalType":"uint256","name":"nonce","type":"uint256"}],"name":"NonceAlreadyUsed","type":"error"},{"inputs":[{"internalType":"address","name":"caller","type":"address"}],"name":"NotAdmin","type":"error"},{"inputs":[{"internalType":"address","name":"caller","type":"address"}],"name":"NotController","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[{"internalType":"address","name":"prizeAddress","type":"address"},{"internalType":"uint256","name":"prizeAmount","type":"uint256"},{"internalType":"uint256","name":"contractBalance","type":"uint256"}],"name":"PrizeAmountExceedsBalance","type":"error"},{"inputs":[{"internalType":"uint32","name":"prizeId","type":"uint32"},{"internalType":"address","name":"user","type":"address"}],"name":"PrizeNotWonByUser","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"SafeERC20FailedOperation","type":"error"},{"inputs":[{"internalType":"uint256","name":"expirationTimestamp","type":"uint256"},{"internalType":"uint256","name":"currentTimestamp","type":"uint256"}],"name":"SignatureExpired","type":"error"},{"inputs":[{"internalType":"address","name":"signer","type":"address"}],"name":"SignerNotAllowed","type":"error"},{"inputs":[{"internalType":"address","name":"prizeAddress","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"TokenNotOwnedByContract","type":"error"},{"inputs":[{"internalType":"uint256","name":"expirationTimestamp","type":"uint256"}],"name":"VrfRequestHasNotExpired","type":"error"},{"anonymous":false,"inputs":[],"name":"EIP712DomainChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"}],"name":"NoPrizeWon","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"requestId","type":"uint256"},{"indexed":false,"internalType":"uint64","name":"nonce","type":"uint64"},{"indexed":false,"internalType":"uint256","name":"expirationTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint64","name":"boost","type":"uint64"}],"name":"Participation","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"requestId","type":"uint256"}],"name":"ParticipationCancelled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint32","name":"prizeId","type":"uint32"}],"name":"PrizeClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint32","name":"prizeId","type":"uint32"}],"name":"PrizeWon","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32[]","name":"newPrizeIds","type":"uint32[]"},{"components":[{"internalType":"uint32","name":"lotAmount","type":"uint32"},{"internalType":"uint64","name":"probability","type":"uint64"},{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256[]","name":"availableERC721Ids","type":"uint256[]"}],"indexed":false,"internalType":"struct ISpinGame.Prize[]","name":"prizes","type":"tuple[]"}],"name":"PrizesUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"round","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"data","type":"bytes"}],"name":"RequestedRandomness","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"signer","type":"address"}],"name":"SignerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"vrfOperator","type":"address"}],"name":"vrfOperatorUpdated","type":"event"},{"inputs":[],"name":"BASE_POINT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"CONTROLLER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_tokenAddress","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"adminWithdrawERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_tokenAddress","type":"address"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"adminWithdrawERC721","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"adminWithdrawNative","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_requestId","type":"uint256"}],"name":"cancelParticipation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"_prizeId","type":"uint32"}],"name":"claimPrize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"eip712Domain","outputs":[{"internalType":"bytes1","name":"fields","type":"bytes1"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"version","type":"string"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"address","name":"verifyingContract","type":"address"},{"internalType":"bytes32","name":"salt","type":"bytes32"},{"internalType":"uint256[]","name":"extensions","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"randomness","type":"uint256"},{"internalType":"bytes","name":"dataWithRound","type":"bytes"}],"name":"fulfillRandomness","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"_prizeId","type":"uint32"}],"name":"getPrize","outputs":[{"components":[{"internalType":"uint32","name":"lotAmount","type":"uint32"},{"internalType":"uint64","name":"probability","type":"uint64"},{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256[]","name":"availableERC721Ids","type":"uint256[]"}],"internalType":"struct ISpinGame.Prize","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPrizesAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"},{"internalType":"uint32[]","name":"_prizeIds","type":"uint32[]"}],"name":"getUserPrizesWon","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"},{"internalType":"uint32","name":"_prizeId","type":"uint32"}],"name":"hasWonPrize","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_signer","type":"address"},{"internalType":"address","name":"_admin","type":"address"},{"internalType":"address","name":"_controller","type":"address"},{"internalType":"address","name":"_vrfOperator","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"forwarder","type":"address"}],"name":"isTrustedForwarder","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nextPrizeId","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint64","name":"nonce","type":"uint64"}],"name":"nonces","outputs":[{"internalType":"bool","name":"used","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"uint256","name":"_expirationTimestamp","type":"uint256"},{"internalType":"uint64","name":"_boost","type":"uint64"},{"components":[{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"},{"internalType":"uint8","name":"v","type":"uint8"}],"internalType":"struct ISpinGame.Signature","name":"_signature","type":"tuple"}],"name":"participate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"prizeIds","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"callerConfirmation","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"requestId","type":"uint256"}],"name":"requestIdTimestamp","outputs":[{"internalType":"uint256","name":"timestamp","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"requestId","type":"uint256"}],"name":"requestIdToUser","outputs":[{"internalType":"address","name":"user","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"requestPending","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"requestedHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"lotAmount","type":"uint32"},{"internalType":"uint64","name":"probability","type":"uint64"},{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256[]","name":"availableERC721Ids","type":"uint256[]"}],"internalType":"struct ISpinGame.Prize[]","name":"_prizes","type":"tuple[]"}],"name":"setPrizes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_signer","type":"address"}],"name":"setSigner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_vrfOperator","type":"address"}],"name":"setVrfOperator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"signer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalProbabilities","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"trustedForwarder","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userToBoost","outputs":[{"internalType":"uint64","name":"boost","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"vrfOperator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]'
    module_name = 'LINEA_WHEEL'
    nft_address = '0xDb3a3929269281F157A58D91289185F21E30A1e0'

    def execute(self, account, chain='LINEA'):
        web3 = init_web3(
            {
                "rpc": "https://rpc.linea.build",
                "poa": "true",
                "chain_id": 59144
            },
            account.proxy
        )
        #sign_wheel(account)
        jwt_token = get_jwt_token(account, web3)
        time.sleep(1)
        linea_auth(jwt_token)
        time.sleep(1)
        data = create_data(jwt_token, web3)
        print(f"DATA {data}")

        Send(
            None,
            web3
        ).send_to_wallet(
            account,
            self.nft_address,
            NativeBalance(0, chain, "ETH"),
            data
        )

    def log(self):
        return "LINEA WHEEL"


def get_jwt_token(account, web3):
    nonce = requests.get("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/nonce")
    # print(f"NONCE {nonce.text}")
    nonce_text = nonce.json()['nonce']

    # Use current timestamp instead of hardcoded one
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    message_to_sign = form_message_to_sign(account, current_time, nonce_text)
    encoded_message_to_sign = encode_defunct(text=message_to_sign)
    signed_message = web3.eth.account.sign_message(encoded_message_to_sign, private_key=account.key)
    # print(f"message to sign: {message_to_sign}")
    # print(f"HASH {signed_message.signature.hex()}")

    signature_hex = signed_message.signature.hex()

    session_pubkey = generate_session_pubkey()
    print(f"SESSION PUBKEY {session_pubkey}")
    params = {
        "signedMessage": f"0x{signature_hex}",
        "messageToSign": message_to_sign,
        "publicWalletAddress": Web3.to_checksum_address(account.address),
        "chain": "EVM",
        "walletName": "metamask",
        "walletProvider": "browserExtension",
        "network": "59144",
        "additionalWalletAddresses": [],
        "sessionPublicKey": session_pubkey
    }

    # Generate unique request ID
    request_id = str(uuid.uuid4()).replace('-', '')

    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7",
        "content-type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0',
        "origin": "https://linea.build",
        "priority": "u=1, i",
        "referer": "https://linea.build/",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "x-dyn-api-version": "API/0.0.681",
        "x-dyn-request-id": request_id,
    }

    result = requests.post(
        "https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/verify",
        json=params,
        headers=headers
    )

    print(f"JWT Auth Status Code: {result.status_code}")
    print(f"JWT Auth Response: {result.text}")

    if result.status_code != 200:
        raise Exception(f"JWT Authentication failed: {result.text}")

    response_data = result.json()
    if "jwt" not in response_data:
        raise Exception(f"JWT token not found in response: {response_data}")

    return response_data["jwt"]


def form_message_to_sign(account, current_time, nonce_text):
    return f"""linea.build wants you to sign in with your Ethereum account:
{Web3.to_checksum_address(account.address)}

Welcome to Linea Hub. Signing is the only way we can truly know that you are the owner of the wallet you are connecting. Signing is a safe, gas-less transaction that does not in any way give Linea Hub permission to perform any transactions with your wallet.

URI: https://linea.build/hub/rewards
Version: 1
Chain ID: 59144
Nonce: {nonce_text}
Issued At: {current_time}
Request ID: ae98b9b4-daaf-4bb3-b5e0-3f07175906ed"""


def linea_auth(bearer_token: str):
    url = "https://hub-api.linea.build/auth"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://linea.build/",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}",
        "Origin": "https://linea.build",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=4",
        "TE": "trailers",
    }

    response = requests.post(url, headers=headers, data=b"")
    response.raise_for_status()  # raise error if status != 200
    return response.json()

# Example usage:
# token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIs..."
# print(linea_auth(token))



def create_data(jwt_token, web3):
    url = "https://hub-api.linea.build/spins"

    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://linea.build/",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
    }

    response = requests.post(url, headers=headers)

    print(f"Spins API Status Code: {response.status_code}")
    print(f"Spins API Response: {response.content}")

    if response.status_code == 404:
        print(f"User not found in Linea Hub system. Address may need to be registered first.")
        raise Exception(f"User not found: {response.text}")
    elif response.status_code != 200:
        try:
            error_msg = response.json().get('message', 'Unknown error')
        except:
            error_msg = response.text
        raise Exception(f"Spins API failed with status {response.status_code}: {error_msg}")

    # Get the JSON response data
    response_data = response.json()
    print(f"Response JSON: {response_data}")

    contract = web3.eth.contract(address=LineaWheel.nft_address, abi=LineaWheel.abi)
    # Convert response data to contract function parameters
    nonce = int(response_data['nonce'])
    expiration_timestamp = int(response_data['expirationTimestamp'])
    boost = int(response_data['boost'])

    # Convert signature array to struct format
    signature_array = response_data['signature']
    signature_struct = {
        'r': signature_array[0],  # bytes32
        's': signature_array[1],  # bytes32  
        'v': int(signature_array[2])  # uint8
    }

    return contract.encode_abi("participate", args=(
        nonce,
        expiration_timestamp,
        boost,
        signature_struct
    ))


def sign_wheel(account):
    url = "https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/connect"

    payload = {
        "address": Web3.to_checksum_address(account.address),
        "chain": "EVM",
        "provider": "browserExtension",
        "walletName": "metamask",
        "authMode": "connect-and-sign"
    }

    response = requests.post(url, json=payload)
    print(f"REGISTER: {response.status_code} {response.content}")


def generate_session_pubkey() -> str:
    # Generate a 32-byte private key
    private_key_bytes = os.urandom(32)

    # Create a private key object
    from eth_keys import keys

    private_key = keys.PrivateKey(private_key_bytes)

    # Get the compressed public key (33 bytes, starts with 02 or 03)
    compressed_pubkey = private_key.public_key.to_compressed_bytes()

    # Return hex string
    return compressed_pubkey.hex()
