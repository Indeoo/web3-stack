from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.tokens import Erc20Token

from web3_wizzard_lib.core.contract.zerolend_contract import ZeroLendContract
from web3_wizzard_lib.core.modules.bank.bank import Bank


class ZeroLend(Bank):
    app_name = 'ZEROLEND'
    supported_chains = ['LINEA']

    def __init__(self, chain, web3):
        self.chain = chain
        self.web3 = web3
        self.contract = ZeroLendContract(get_contracts_for_chain(self.chain)['ZEROLEND_LEND'], self.web3)

    def supply(self, account, amount):
        logger.info(f"Deposit {amount} to ZEROLEND")

        self.contract.deposit_eth(account, amount.wei)

    def redeem(self, account, amount):
        erc20_token = Erc20Token('LINEA', get_tokens_for_chain(self.chain)['ZEROLEND_WETH'], self.web3)

        if erc20_token.allowance(account, self.contract.contract_address) < 100:
            erc20_token.approve(account, self.contract.contract_address)

        self.contract.withdraw_eth(account, amount.wei)

    def get_deposit_amount(self, account, token):
        erc20_token = Erc20Token('LINEA', get_tokens_for_chain(self.chain)['ZEROLEND_WETH'], self.web3)

        return erc20_token.balance(account)

