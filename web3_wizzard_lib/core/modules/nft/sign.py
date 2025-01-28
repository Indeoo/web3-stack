from json import dumps

import requests
from eth_account.messages import encode_defunct


def sign_in_message(account, web3):
    message_text = "Please sign this message to confirm you are the owner of this address and Sign in to TrustGo App"
    signature = sign_msg(account, message_text, web3)
    url = 'https://mp.trustalabs.ai/accounts/check_signed_message'
    data = {
        "mode": "evm", "address": account.address,
        "message": message_text,
        "signature": signature,
        "invite_from": {"from": "0", "code": 'EPR0QD9W52I8'}}
    headers = {'Authorization': f'TOKEN null', 'Accept': 'application/json'}
    data_json = dumps(data)
    r = requests.post(url, data=data_json, headers=headers)
    if r.status_code == 200:
        res = [r.json()]
        if res[0]['code'] == 0:
            token_auth = res[0]['data']['token']
            return token_auth
    return -1


def sign_msg(wallet, message_text, web3):
    text_hex = "0x" + message_text.encode('utf-8').hex()
    text_encoded = encode_defunct(hexstr=text_hex)
    signed_message = web3.eth.account.sign_message(text_encoded, private_key=wallet.key)
    signature = signed_message.signature
    return signature.hex()