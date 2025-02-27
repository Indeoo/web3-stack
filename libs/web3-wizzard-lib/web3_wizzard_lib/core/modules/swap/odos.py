from loguru import logger
from sybil_engine.domain.dex import Dex
from sybil_engine.utils.retry import retry
from sybil_engine.utils.utils import AccountException

from web3_wizzard_lib.core.contract.odos import Odos


class OdosSwap(Dex):
    dex_name = 'odos'
    swap_contract = 'ODOS'
    supported_chains = ['ZKSYNC', 'BASE', 'LINEA', 'ARBITRUM']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.odos_router_contract = self.chain_contracts[self.swap_contract]
        self.odos_router = Odos(self.odos_router_contract, self.web3)

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def swap(self, amount_to_swap, from_token, to_token, slippage, account):
        logger.info(
            f"Swap {amount_to_swap.log_line()}->{to_token.symbol()} in {self.dex_name} ({self.chain_instance['chain']})")

        if amount_to_swap.token == 'ETH':
            from_token_address = '0x0000000000000000000000000000000000000000'
        else:
            from_token_address = from_token.erc20_contract.contract_address

        if to_token.token == 'ETH':
            to_token_address = '0x0000000000000000000000000000000000000000'
        else:
            to_token_address = to_token.erc20_contract.contract_address

        quote_data = self.odos_router.quote(
            account, from_token_address, to_token_address, amount_to_swap.wei, slippage, self.chain_instance['chain']
        )

        if amount_to_swap.token == 'ETH':
            transaction_data = self.odos_router.assemble(account, quote_data["pathId"])

            func = self.odos_router.swap
        else:
            balance = from_token.balance(account)

            if balance.wei < amount_to_swap.wei:
                raise AccountException(f"Balance {balance} < {amount_to_swap}")

            if from_token.allowance(account, self.odos_router_contract) < amount_to_swap.wei:
                from_token.approve(account, self.odos_router_contract)

            transaction_data = self.odos_router.assemble(account, quote_data["pathId"])

            if to_token.token == 'ETH':
                func = self.odos_router.swap
            else:
                raise Exception('Not supported')

        func(account, transaction_data)
