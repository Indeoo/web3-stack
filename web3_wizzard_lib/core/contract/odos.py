import requests
from sybil_engine.config.app_config import get_network

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi
from sybil_engine.utils.utils import SwapException

abi = load_abi("resources/abi/lineaswap_router.json")

referral = {
    324: 387663447,
    260: 387663447,
    8453: 1030612943,
    18453: 1030612943,
    59144: 268273819
}

chain_map_id = {
    'BASE': 8453,
    'ZKSYNC': 324
}


class Odos(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def quote(self, account, from_token: str, to_token: str, amount: int, slippage: float, chain: str):
        chain_id = self.get_chain_id(chain)

        url = "https://api.odos.xyz/sor/quote/v2"

        data = {
            "chainId": chain_id,
            "inputTokens": [
                {
                    "tokenAddress": from_token,
                    "amount": f"{amount}"
                }
            ],
            "outputTokens": [
                {
                    "tokenAddress": to_token,
                    "proportion": 1
                }
            ],
            "slippageLimitPercent": slippage,
            "userAddr": account.address,
            "referralCode": referral[self.web3.eth.chain_id] if True is True else 0,
            "compact": True
        }

        response = self.proxy_request(account, data, url)

        if response.status_code == 200:
            return response.json()
        else:
            raise SwapException(f"[{account.app_id}][{account.address}] Bad Odos request")

    def assemble(self, account, path_id):
        url = "https://api.odos.xyz/sor/assemble"

        data = {
            "userAddr": account.address,
            "pathId": path_id,
            "simulate": False,
        }

        response = self.proxy_request(account, data, url)

        if response.status_code == 200:
            return response.json()
        else:
            raise SwapException(f"[{account.app_id}][{account.address}] Bad Odos request")

    def proxy_request(self, account, data, url):
        proxies = {}
        proxies.update(
            {"http": account.proxy}
        )
        response = requests.post(
            url=url,
            headers={"Content-Type": "application/json"},
            json=data,
            proxies=proxies
        )
        return response

    @evm_transaction
    def swap(self, account, transaction_data):
        transaction = transaction_data["transaction"]

        transaction["nonce"] = self.web3.eth.get_transaction_count(transaction['from'])
        transaction["chainId"] = self.web3.eth.chain_id
        transaction["value"] = int(transaction["value"])

        return transaction

    def get_chain_id(self, chain):
        if get_network() == 'MAIN':
            return self.web3.eth.chain_id
        else:
            return chain_map_id[chain]
