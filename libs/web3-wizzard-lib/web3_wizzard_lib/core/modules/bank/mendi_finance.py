from loguru import logger
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.tokens import Erc20Token

from web3_wizzard_lib.core.contract.mendi_token import MendiTokenContract
from web3_wizzard_lib.core.modules.bank.bank import Bank


class MendiFinance(Bank):
    app_name = 'MENDI_FINANCE'
    supported_chains = ['LINEA']

    def __init__(self, chain, web3):
        self.chain = chain
        self.web3 = web3

    def supply(self, account, amount):
        erc20 = Erc20Token(self.chain, amount.token, self.web3)
        amount = erc20.balance(account)

        me_token = f'me{amount.token}'
        mendi_token_address = get_tokens_for_chain(self.chain)[me_token]

        logger.info(f"Mendi supply {amount} {amount.token}")

        if erc20.allowance(account, mendi_token_address) < erc20.balance(account).wei:
            erc20.approve(account, mendi_token_address)

        mendi = MendiTokenContract(mendi_token_address, self.web3)
        mendi.mint(account, amount.wei)

    def borrow(self, account, amount):
        logger.info(f"Mendi borrow {amount.token}")

    def repay_borrow(self, account, amount):
        logger.info(f"Mendi repay {amount.token}")

    def redeem(self, account, amount):
        me_token = f'me{amount.token}'
        mendi_token_address = get_tokens_for_chain(self.chain)[me_token]
        mendi = MendiTokenContract(mendi_token_address, self.web3)

        redeem_balance = mendi.balance_of(account)

        if redeem_balance > 1000000000:
            logger.info(f"Mendi reedem {amount. token}")
            mendi.redeem(account, redeem_balance)
        else:
            logger.info(f"Mendi balance is 0")

    def get_deposit_amount(self, account, token):
        #me_token = f'meweETH'
        mendi_token_address = get_tokens_for_chain(self.chain)[token]
        mendi = MendiTokenContract(mendi_token_address, self.web3)

        return mendi.balance_of(account)

