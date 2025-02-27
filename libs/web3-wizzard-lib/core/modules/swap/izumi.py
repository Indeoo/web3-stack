from sybil_engine.domain.dex import Dex

from ...contract.izumi import IzumiRouter


class Izumi(Dex):
    dex_name = 'izumi'
    swap_contract = 'IZUMI'
    supported_chains = ['LINEA']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.weth_address = self.tokens['WETH']
        self.izumi = IzumiRouter(self.chain_contracts[self.swap_contract], self.web3)

    def swap_token_for_native(self, account, amount_to_swap, from_token_address, slippage):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, from_token_address, self.weth_address) * slippage)
        args = [account, amount_to_swap, amount_out_min, from_token_address, self.weth_address]
        func = self.izumi.multicall

        return args, func

    def swap_native_for_token(self, account, amount_to_swap, slippage, to_token_address):
        amount_out_min = int(self.get_amount_out_min(amount_to_swap, self.weth_address, to_token_address) * slippage)
        args = [account, amount_to_swap, amount_out_min, self.weth_address, to_token_address]
        func = self.izumi.multicall

        return args, func

    def swap_token_for_token(self, account, amount_to_swap, slippage, from_token_address, to_token_address):
        raise Exception("Not supported yet")

    def get_amount_out_min(self, amount_to_swap, from_token_address, to_token_address):
        izumi = self.chain_contracts["IZUMI"]
        izumi_router = IzumiRouter(izumi, self.web3)

        if amount_to_swap.token == 'ETH':
            return int((izumi_router.quote_price('weETH') * amount_to_swap.wei) * 0.999)
        else:
            return int((izumi_router.quote_price('ETH') * amount_to_swap.wei) * 0.999)

