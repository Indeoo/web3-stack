import inspect

from web3 import Web3

from sybil_engine.contract.erc20contract import Erc20Contract
from sybil_engine.contract.weth import WETH
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.balance import Erc20Balance, WETHBalance


class Erc20Token:
    def __init__(self, chain, token, web3):
        self.chain = chain
        self.token = token
        self.web3 = web3

        if not Web3.is_address(token):
            token = get_tokens_for_chain(self.chain)[self.token]

        self.erc20_contract = Erc20Contract(token, self.web3)

    def balance(self, account):
        return Erc20Balance(
            self.erc20_contract.balance_of(account),
            self.chain,
            self.token,
            decimal=self.erc20_contract.decimals()
        )

    def approve(self, account, contract_on_approve):
        caller_frame = inspect.currentframe().f_back
        caller_function = caller_frame.f_code.co_name
        if caller_function == 'execute_transaction_internal':
            original_function = self.erc20_contract.approve.__wrapped__ if hasattr(self.erc20_contract.approve,
                                                                                   "__wrapped__") else self.erc20_contract.approve
            return original_function(self.erc20_contract, account, contract_on_approve)
        else:
            return self.erc20_contract.approve(account, contract_on_approve)

    def allowance(self, account, allowance_contract):
        return self.erc20_contract.allowance(account, allowance_contract)

    def transfer(self, amount, receive_address, account):
        self.erc20_contract.transfer(account, amount, receive_address)

    def symbol(self):
        if self.erc20_contract.contract_address == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
            return 'ETH'
        else:
            return self.erc20_contract.symbol()

    def address(self):
        return self.erc20_contract.contract_address


class WETHToken:
    def __init__(self, chain, web3):
        self.chain = chain
        self.web3 = web3
        self.weth_contract = WETH(get_tokens_for_chain(self.chain)['WETH'], self.web3)

    def balance(self, account):
        return WETHBalance(self.weth_contract.balance_of(account), self.chain)
