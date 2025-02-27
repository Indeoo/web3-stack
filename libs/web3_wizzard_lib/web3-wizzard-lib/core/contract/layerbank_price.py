from sybil_engine.contract.contract import Contract
from sybil_engine.data.networks import get_ids_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/layerbank_price.json")


class LayerBankPrice(Contract):
    def __init__(self, contract_address, web3):
        self.weth_token = get_tokens_for_chain(get_ids_chain()[web3.eth.chain_id])['WETH']
        super().__init__(contract_address, web3, abi)

    def get_underlying_price(self, token):
        return self.contract.functions.getUnderlyingPrice(token).call()

    def price_of_eth(self):
        return self.contract.functions.priceOfETH().call()
