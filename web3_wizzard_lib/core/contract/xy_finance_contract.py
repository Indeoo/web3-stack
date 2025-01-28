import requests
from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from web3 import Web3


class XYSwapContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, None)

    def get_quote(self, from_token: str, to_token: str, amount: int, slippage: float):
        url = "https://aggregator-api.xy.finance/v1/quote"

        params = {
            "srcChainId": self.web3.eth.chain_id,
            "srcQuoteTokenAddress": Web3.to_checksum_address(from_token),
            "srcQuoteTokenAmount": amount.wei,
            "dstChainId": self.web3.eth.chain_id,
            "dstQuoteTokenAddress": Web3.to_checksum_address(to_token),
            "slippage": slippage
        }

        response = requests.get(url=url, params=params)
        transaction_data = response.json()

        return transaction_data

    @evm_transaction
    def swap(
            self,
            account,
            amount_to_swap,
            from_token: str,
            to_token: str,
            quote: int,
            slippage: int
    ):
        amount_wei = amount_to_swap.wei

        swap_provider = quote["routes"][0]["srcSwapDescription"]["provider"]

        transaction_data = self.build_transaction(
            account,
            from_token,
            to_token,
            amount_wei,
            slippage,
            swap_provider
        )

        tx_data = self.build_generic_data(account.address, True)

        tx_data.update(
            {
                "to": self.web3.to_checksum_address(transaction_data["tx"]["to"]),
                "data": transaction_data["tx"]["data"],
                "value": transaction_data["tx"]["value"],
                "nonce": self.web3.eth.get_transaction_count(account.address)
            }
        )

        return tx_data

    def build_transaction(self, account, from_token: str, to_token: str, amount: int, slippage: float,
                          swap_provider: str):
        url = "https://aggregator-api.xy.finance/v1/buildTx"

        params = {
            "srcChainId": self.web3.eth.chain_id,
            "srcQuoteTokenAddress": Web3.to_checksum_address(from_token),
            "srcQuoteTokenAmount": amount,
            "dstChainId": self.web3.eth.chain_id,
            "dstQuoteTokenAddress": Web3.to_checksum_address(to_token),
            "slippage": slippage,
            "receiver": account.address,
            "srcSwapProvider": swap_provider,
        }

        # if XYSWAP_CONTRACT["use_ref"]:
        #     params.update({
        #         "affiliate": Web3.to_checksum_address("0xb98308D11E2B578858Fbe65b793e71C7a0CAa43e"),
        #         "commissionRate": 10000
        #     })

        response = requests.get(url=url, params=params)

        return response.json()
