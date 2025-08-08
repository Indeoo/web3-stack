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
    from sybil_engine.utils.file_loader import load_abi

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
    abi = load_abi("resources/abi/linea_wheel/abi.json")
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
