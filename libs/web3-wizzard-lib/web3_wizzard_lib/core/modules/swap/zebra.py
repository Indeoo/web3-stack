from sybil_engine.domain.dex import Dex

from web3_wizzard_lib.core.contract.zebra_contract import ZebraContract


class Zebra(Dex):
    dex_name = 'zebra'
    swap_contract = "ZEBRA"
    supported_chains = ['SCROLL']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.weth_address = self.tokens['WETH']
        zebra_contract = self.chain_contracts[self.swap_contract]
        self.zebra = ZebraContract(zebra_contract, self.web3)

    def swap_native_for_token(self, account, amount_to_swap, slippage, to_token_address):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, self.tokens['ETH'], to_token_address) * slippage)

        args = [account, amount_to_swap, self.tokens['ETH'], to_token_address, amount_out_min]
        func = self.zebra.swap_to_token
        return args, func

    def swap_token_for_native(self, account, amount_to_swap, from_token_address, slippage):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, from_token_address, self.weth_address) * slippage)

        args = [account, amount_to_swap, from_token_address, self.tokens['ETH'], amount_out_min]
        func = self.zebra.swap_to_eth
        return args, func

    def get_amount_out_min(self, amount_to_swap, from_token_address, to_token_address):
        return self.zebra.get_min_amount_out(amount_to_swap, from_token_address, to_token_address)
