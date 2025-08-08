import requests
from eth_account.messages import encode_defunct

from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


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
        jwt_token = get_jwt_token(account, web3)
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
    from datetime import datetime, timezone

    nonce = requests.get("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/nonce")
    print(f"NONCE {nonce.text}")
    nonce_text = nonce.json()['nonce']

    # Use current timestamp instead of hardcoded one
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    message_to_sign = f"""linea.build wants you to sign in with your Ethereum account:
{account.address}

Welcome to Linea Hub. Signing is the only way we can truly know that you are the owner of the wallet you are connecting. Signing is a safe, gas-less transaction that does not in any way give Linea Hub permission to perform any transactions with your wallet.

URI: https://linea.build/hub/rewards
Version: 1
Chain ID: 59144
Nonce: {nonce_text}
Issued At: {current_time}
Request ID: ae98b9b4-daaf-4bb3-b5e0-3f07175906ed"""
    print(f"message to sign: {message_to_sign}")
    encoded_message_to_sign = encode_defunct(text=message_to_sign)
    signed_message = web3.eth.account.sign_message(encoded_message_to_sign, private_key=account.key)

    print(f"HASH {signed_message.signature.hex()}")

    # Try without the 0x prefix for the signature
    signature_hex = signed_message.signature.hex()
    if signature_hex.startswith('0x'):
        signature_hex = signature_hex[2:]
    params = {
        "signedMessage": f"0x{signature_hex}",
        "messageToSign": message_to_sign,
        "publicWalletAddress": account.address,
        "chain": "EVM",
        "walletName": "metamask",
        "walletProvider": "browserExtension",
        "network": "59144",
        "additionalWalletAddresses": []
        # Removed sessionPublicKey - it's likely causing the verification failure
    }

    result = requests.post("https://app.dynamicauth.com/api/v0/sdk/ae98b9b4-daaf-4bb3-b5e0-3f07175906ed/verify",
                           json=params)

    print(result)
    print(result.text)

    return result.json()["jwt"]


def create_data(jwt_token, web3):
    import requests

    url = "https://hub-api.linea.build/spins"

    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://linea.build/",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
        "Origin": "https://linea.build",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=0",
        "Content-Length": "0",
        "TE": "trailers"
    }

    response = requests.post(url, headers=headers)

    print("Status code:", response.status_code)
    print("Response body:", response.content)

    if response.status_code != 200:
        raise Exception(response.json()['message'])
    
    # Get the JSON response data
    response_data = response.json()
    print(f"Response JSON: {response_data}")
    
    # Load LineaWheel contract ABI and create contract instance
    abi = LineaWheel.abi
    contract_address = '0xDb3a3929269281F157A58D91289185F21E30A1e0'  # LineaWheel contract address
    contract = web3.eth.contract(address=contract_address, abi=abi)
    
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
    
    # Encode the participate function call
    encoded_data = contract.encode_abi("participate", args=(
        nonce,
        expiration_timestamp, 
        boost,
        signature_struct
    ))
    
    return encoded_data
