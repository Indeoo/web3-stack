from loguru import logger
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.domain.dex import Dex
from sybil_engine.utils.gas_utils import l1_gas_price
from sybil_engine.utils.utils import AccountException

from web3_wizzard_lib.core.contract.xy_finance_contract import XYSwapContract


class XyFinance(Dex):
    dex_name = 'xy.finance'
    swap_contract = 'XY_FINANCE'
    supported_chains = ['SCROLL']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.contract_address = self.chain_contracts[self.swap_contract]
        self.xy_swap_contract = XYSwapContract(self.contract_address, self.web3)

    @l1_gas_price
    def swap(self, amount_to_swap, from_token, to_token, slippage, account):
        if amount_to_swap.wei == 0:
            raise AccountException(f"{amount_to_swap.token} balance is 0")

        token_in_address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE" if from_token == "ETH" else self.tokens[from_token]
        token_out_address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE" if to_token == "ETH" else self.tokens[to_token]

        logger.info(f"Swap {amount_to_swap.log_line()}->{to_token} in {self.dex_name} ({self.chain_instance['chain']})")

        erc20_from_token = Erc20Token(self.chain_instance['chain'], amount_to_swap.token, self.web3)

        if amount_to_swap.token != 'ETH':
            if erc20_from_token.allowance(account, self.contract_address) < amount_to_swap.wei:
                erc20_from_token.approve(account, self.contract_address)

        slippage = int((1 - slippage) * 100)

        amount_out_min = self.get_amount_out_min(amount_to_swap, token_in_address, token_out_address, slippage)

        self.xy_swap_contract.swap(account, amount_to_swap, token_in_address, token_out_address, amount_out_min, slippage)

    def get_amount_out_min(self, amount_to_swap, token_in_address, token_out_address, slippage):
        return self.xy_swap_contract.get_quote(token_in_address, token_out_address, amount_to_swap, slippage)
