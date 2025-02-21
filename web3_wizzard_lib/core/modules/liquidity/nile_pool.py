from loguru import logger
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.balance_utils import interval_to_eth_balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.utils.retry import retry

from web3_wizzard_lib.core.contract.nile_contract import NileContract
from web3_wizzard_lib.core.modules.liquidity.pool import Pool


class NilePool(Pool):
    pool_contract = 'NILE_POOL'

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.nile_contract = NileContract(self.velocore_pool_contract_address, self.web3)

    @retry(max_attempts=2, retry_interval={'from': 10, 'to': 20})
    def deposit(self, amount_interval, account, token, min_native_balance, chain):
        amount = interval_to_eth_balance(amount_interval, account, chain, self.web3)

        pool_amount = self.nile_contract.get_amount_out(
            amount,
            get_tokens_for_chain(chain)['WETH'],
            get_tokens_for_chain(chain)[token]
        )[0]

        nile_token = Erc20Token(chain, token, self.web3)

        if nile_token.allowance(account, self.nile_contract.contract_address) < nile_token.balance(account).wei:
            nile_token.approve(account, self.nile_contract.contract_address)

        logger.info(f"Deposit {amount} and {nile_token.balance(account)}")
        self.nile_contract.add_liquidity_eth(account, nile_token.erc20_contract.contract_address, pool_amount, amount)

    @retry(max_attempts=2, retry_interval={'from': 10, 'to': 20})
    def withdraw(self, account, token, chain):
        weth_zero_address = get_tokens_for_chain(chain)[f"WETH_{token}_LP"]

        weth_zero = Erc20Token(chain, weth_zero_address, self.web3)

        if weth_zero.balance(account).wei < 10000:
            logger.info("NILE almost zero balance")

        zero_token_address = get_tokens_for_chain(chain)[token]

        amount = self.nile_contract.quote_remove_liquidity_eth(
            get_tokens_for_chain(chain)['WETH'],
            get_tokens_for_chain(chain)[token],
            weth_zero.balance(account).wei
        )

        if weth_zero.allowance(account, self.nile_contract.contract_address) < weth_zero.balance(account).wei:
            weth_zero.approve(account, self.nile_contract.contract_address)

        logger.info(f"Withdraw {token} on NILE {weth_zero.balance(account)}")

        self.nile_contract.remove_liquidity_eth(
            account,
            zero_token_address,
            weth_zero.balance(account).wei,
            amount[0],
            amount[1]
        )
