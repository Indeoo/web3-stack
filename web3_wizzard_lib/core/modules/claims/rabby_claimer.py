import time
from random import randint

from eth_account.messages import encode_defunct, SignableMessage
from fake_useragent import UserAgent
from loguru import logger

import requests
from sybil_engine.utils.utils import randomized_sleeping

url = "https://api.rabby.io/v2/points/claim_snapshot"

headers = {
    "Host": "api.rabby.io",
    "Connection": "keep-alive",
    "Content-Length": "224",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "X-Version": "0.92.48",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": UserAgent().random,
    "x-api-ts": str(int(time.time())),
    "Content-Type": "application/json",
    "x-api-ver": "v2",
    "Accept": "application/json, text/plain, */*",
    "X-Client": "Rabby",
    "sec-ch-ua-platform": '"Windows"',
    "Origin": "chrome-extension://acmacodkjb dgmoleebolmdjonilkdbch",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
}


def claimer_rabby(account, web3):
    try:
        address = account.address.lower()
        msg = f"{address} Claims Rabby Points"

        payload = {
            "id": address,
            "signature": get_signed_code(web3, account, msg),
            "invite_code": "FREEBONUS"
        }

        proxies = {}
        proxies.update(
            {"http": account.proxy,
            "https": account.proxy}
        )

        response = make_request_with_retries(url, headers=headers, json=payload, proxies=proxies)

        if response.json().get("error_code") == 0:
            logger.success(f"{address} | Claimed!")
        else:
            resp_msg = response.json().get("error_msg")
            logger.info(f"{address} | {resp_msg} | {response.json()}")
    except Exception as e:
        logger.error(f"{account}... | {e}")


def sign(web3, account, encoded_msg: SignableMessage):
    return web3.eth.account.sign_message(encoded_msg, account.key)


def get_signed_code(web3, account, msg) -> str:
    return sign(web3, account, encode_defunct(text=msg)).signature.hex()

def make_request_with_retries(url, headers, json, proxies, max_retries=5):
    for attempt in range(max_retries):
        response = requests.post(url, headers=headers, json=json, proxies=proxies)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", randint(1, 5)))
            logger.info(f"Rate limited. Retrying after {retry_after} seconds. Attempt {attempt + 1}/{max_retries}")
            time.sleep(retry_after)
        else:
            return response
    logger.error("Max retries reached. Giving up.")
    return None