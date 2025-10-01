import random

import requests
from loguru import logger
from sybil_engine.contract.send import Send

from sybil_engine.domain.dex import Dex
from sybil_engine.utils.retry import retry


class MetamuskSwap(Dex):
    dex_name = 'metamusk'
    swap_contract = 'METAMUSK'
    supported_chains = ['ETH_MAINNET', 'BASE']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.send = Send(None, self.web3)
        self.metamusk_router_address = self.chain_contracts[self.swap_contract]

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def swap(self, amount_to_swap, from_token, to_token, slippage, account):
        logger.info(
            f"Swap {amount_to_swap.log_line()}->{to_token.symbol()} in {self.dex_name} ({self.chain_instance['chain']})")

        if amount_to_swap.token == 'ETH':
            from_token_address = '0x0000000000000000000000000000000000000000'
        else:
            if from_token.allowance(account, self.metamusk_router_address) < amount_to_swap.wei:
                from_token.approve(account, self.metamusk_router_address)

            from_token_address = from_token.erc20_contract.contract_address

        if to_token.token == 'ETH':
            to_token_address = '0x0000000000000000000000000000000000000000'
        else:
            to_token_address = to_token.erc20_contract.contract_address

        data = self.get_trade_data(account, amount_to_swap.wei, from_token_address, to_token_address)

        self.send.send_to_wallet(account, self.metamusk_router_address, amount_to_swap, data)

    def get_trade_data(self, account, amount_to_swap_wei, from_token_address, to_token_address):
        response = requests.get(
            "https://bridge.api.cx.metamask.io/getQuote",
            params={
                "walletAddress": account.address,
                "destWalletAddress": account.address,
                "srcChainId": self.chain_instance['chain_id'],
                "destChainId": self.chain_instance['chain_id'],
                "srcTokenAddress": from_token_address,
                "destTokenAddress": to_token_address,
                "srcTokenAmount": amount_to_swap_wei,
                "insufficientBal": True,
                "resetApproval": False,
                "gasIncluded": True,
                "slippage": 2
            }
        )

        choice = random.choice(response.json())
        data = choice['trade']['data']
        return data
