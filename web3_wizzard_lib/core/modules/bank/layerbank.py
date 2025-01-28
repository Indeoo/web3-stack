from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.tokens import Erc20Token

from web3_wizzard_lib.core.contract.layerbank_price import LayerBankPrice
from web3_wizzard_lib.core.contract.layerbank_token import LayerBankToken
from web3_wizzard_lib.core.contract.layerbankcontract import LayerBankContract
from web3_wizzard_lib.core.modules.bank.bank import Bank


class LayerBank(Bank):
    app_name = 'LAYERBANK'
    supported_chains = ['LINEA']

    def __init__(self, chain, web3):
        self.chain = chain
        self.web3 = web3
        self.layerbank = LayerBankContract(get_contracts_for_chain(chain)["LAYERBANK"], web3)

        lbwstETH = get_tokens_for_chain(chain)['lbwstETH']
        self.lbWstETHToken = LayerBankToken(lbwstETH, web3)

        lbETH = get_tokens_for_chain(chain)['lbETH']
        self.lbETHToken = LayerBankToken(lbETH, web3)

    def supply(self, account, token):
        token = LayerBankToken(get_tokens_for_chain(self.chain)[token], self.web3)

        erc20_token = Erc20Token(self.chain, token, self.web3)
        amount = erc20_token.balance(account)

        if 25 * token.one_decimal() <= self.layerbank.account_liquidity_of(account)[0]:
            logger.info("Already supplied over 25$ worth, skip this step")
            return

        if erc20_token.allowance(account, token.contract_address) < amount.wei:
            erc20_token.approve(account, token.contract_address)

        if amount.wei > 0:
            if token.contract_address not in self.layerbank.market_list_of(account):
                logger.info("Add support wstETH to LayerBank")
                self.layerbank.enter_markets(account, token.contract_address)

            logger.info(f"Supply {amount.log_line()}")

            self.layerbank.supply(account, token.contract_address, amount.wei)

        if 25 * token.one_decimal() > self.layerbank.account_liquidity_of(account)[0]:
            raise Exception(
                f"Not enough supply for 25$ borrow {self.layerbank.account_liquidity_of(account)[0] / token.one_decimal()}"
            )

    def borrow(self, account, token):
        token = LayerBankToken(get_tokens_for_chain(self.chain)[token], self.web3)

        layerbank_price = LayerBankPrice(get_contracts_for_chain(self.chain)["LAYERBANK_PRICE"], self.web3)

        usd_collateral = self.layerbank.account_liquidity_of(account)[0]
        eth_amount = (usd_collateral / layerbank_price.get_underlying_price(token.contract_address))

        logger.info(f"Borrow {eth_amount} {token.symbol()}")

        borrow_amount = int(
            eth_amount * token.one_decimal() * token.one_decimal() / token.exchange_rate())

        self.layerbank.borrow(
            account,
            token.contract_address,
            borrow_amount
        )

    def repay_borrow(self, account, token):
        token = LayerBankToken(get_tokens_for_chain(self.chain)[token], self.web3)

        layerbank_price = LayerBankPrice(get_contracts_for_chain(self.chain)["LAYERBANK_PRICE"], self.web3)

        borrowed_usdc = self.layerbank.account_liquidity_of(account)[2]
        lbETHPrice = layerbank_price.get_underlying_price(token.contract_address)
        ethAmount = int(
            (
                    borrowed_usdc / lbETHPrice) * token.one_decimal() * token.one_decimal() / token.exchange_rate()
        )

        if 2 * token.one_decimal() > borrowed_usdc:
            logger.info("Less than 2$ borrowed, skip")
            return

        logger.info(f"Repay Borrow {ethAmount / token.one_decimal()}")
        self.layerbank.repay_borrow(account, token.contract_address, ethAmount)

    def redeem(self, account, amount, token):
        if token == 'ETH':
            token = self.lbETHToken
        elif token == 'wstETH':
            token = self.lbWstETHToken

        underlying_balance = self.get_deposit_amount(account, token)

        if underlying_balance < 10000:
            logger.info("Less than 0.001$ supplied, skip")
            return

        self.layerbank.redeem_token(
            account,
            token.contract_address,
            int(underlying_balance * token.one_decimal() * 0.999 / token.exchange_rate())
        )

    def get_deposit_amount(self, account, token):
        if token == 'ETH':
            token = self.lbETHToken
        elif token == 'wstETH':
            token = self.lbWstETHToken

        return token.underlying_balance_of(account)
