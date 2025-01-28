from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/layerbank_token.json")

MAX_ALLOWANCE = 115792089237316195423570985008687907853269984665640564039457584007913129639935


class LayerBankToken(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def balance_of(self, account):
        return self.contract.functions.balanceOf(account.address).call()

    def underlying_balance_of(self, account):
        return self.contract.functions.balanceOf(account.address).call()

    def exchange_rate(self):
        return self.contract.functions.exchangeRate().call()

    def decimals(self):
        return self.contract.functions.decimals().call()

    def one_decimal(self):
        return 10 ** self.contract.functions.decimals().call()

    def symbol(self):
        return self.contract.functions.symbol().call()
