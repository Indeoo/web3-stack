from loguru import logger

from sybil_engine.config.app_config import get_dex_retry_interval
from sybil_engine.contract.transaction_executor import TransactionExecutionException, execute_transaction
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.balance import NotEnoughERC20Balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.utils.gas_utils import l1_gas_price
from sybil_engine.utils.retry import retry_self
from sybil_engine.utils.utils import SwapException, AccountException


class Dex:
    dex_name = None
    swap_contract = None

    def __init__(self, chain_instance, web3, sleep_interval=None):
        self.chain_contracts = get_contracts_for_chain(chain_instance['chain'])
        self.tokens = get_tokens_for_chain(chain_instance['chain'])
        self.chain_instance = chain_instance
        self.web3 = web3

        if sleep_interval is None:
            self.retry_interval = get_dex_retry_interval()
        else:
            self.retry_interval = sleep_interval

    @retry_self(max_attempts=3, expected_exception=TransactionExecutionException)
    @l1_gas_price
    def swap(self, amount_to_swap, from_token, to_token, slippage, account):
        if amount_to_swap.wei == 0 and amount_to_swap.token != self.chain_instance['gas_token']:
            raise NotEnoughERC20Balance(f"Can't swap {amount_to_swap.log_line()}")

        logger.info(
            f"Swap {amount_to_swap.log_line()}->{to_token.symbol()} in {self.dex_name} ({self.chain_instance['chain']})")

        if from_token.symbol() == 'ETH':
            args, func = self.swap_native_for_token(account, amount_to_swap, slippage, to_token.address())
        else:
            erc20_token = Erc20Token(self.chain_instance['chain'], from_token.address(), self.web3)
            balance = erc20_token.balance(account)
            if balance.wei < amount_to_swap.wei:
                raise AccountException(f"Balance {balance.log_line()}<-{amount_to_swap.log_line()}")

            swap_contract = self.chain_contracts[self.swap_contract]

            if erc20_token.allowance(account, swap_contract) < amount_to_swap.wei:
                erc20_token.approve(account, swap_contract)

            if to_token.symbol() == 'ETH':
                args, func = self.swap_token_for_native(account, amount_to_swap, from_token.address(), slippage)
            else:
                args, func = self.swap_token_for_token(
                    account,
                    amount_to_swap,
                    slippage,
                    from_token.address(),
                    to_token.address()
                )

        if hasattr(func, "__wrapped__"):
            func(*args)
        else:
            execute_transaction(func, args, self.chain_instance, account)

    def swap_token_for_native(self, account, amount_to_swap, from_token_address, slippage):
        raise SwapException("Not supported yet")

    def swap_native_for_token(self, account, amount_to_swap, slippage, to_token_address):
        raise SwapException("Not supported yet")

    def swap_token_for_token(self, account, amount_to_swap, slippage, from_token_address, to_token_address):
        raise SwapException("Not supported yet")

    def get_amount_out_min(self, amount_to_swap, from_token_address, to_token_address):
        raise SwapException("Not supported yet")
