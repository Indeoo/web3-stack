from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.domain.dex import Dex
from sybil_engine.utils.gas_utils import l1_gas_price
from sybil_engine.utils.utils import AccountException

from web3_wizzard_lib.core.contract.woofi_swap import WoofiSwap


class Woofi(Dex):
    dex_name = 'woofi'
    swap_contract = 'WOOFI'
    supported_chains = ['ZKSYNC', 'BASE', 'LINEA', 'ARBITRUM']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.contract_address = self.chain_contracts[self.swap_contract]
        self.woofi_swap = WoofiSwap(self.contract_address, self.web3)

    @l1_gas_price
    def swap(self, amount_to_swap, from_token, to_token, slippage, account):
        if amount_to_swap.wei == 0:
            raise AccountException(f"{amount_to_swap.token} balance is 0")

        token_in_address = self.tokens[amount_to_swap.token]
        token_out_address = self.tokens[to_token.token]

        erc20_from_token = Erc20Token(self.chain_instance['chain'], amount_to_swap.token, self.web3)

        if amount_to_swap.token != 'ETH':
            if erc20_from_token.allowance(account, self.contract_address) < amount_to_swap.wei:
                erc20_from_token.approve(account, self.contract_address)

        amount_out_min = int(self.get_amount_out_min(amount_to_swap, token_in_address, token_out_address) * slippage)

        self.woofi_swap.swap(account, amount_to_swap, token_in_address, token_out_address, amount_out_min)

    def get_amount_out_min(self, amount_to_swap, token_in_address, token_out_address):
        return self.woofi_swap.query_swap(token_in_address, token_out_address, amount_to_swap)
