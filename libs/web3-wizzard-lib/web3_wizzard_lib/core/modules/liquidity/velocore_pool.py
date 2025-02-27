from loguru import logger
from sybil_engine.domain.balance.balance_utils import interval_to_eth_balance, interval_to_erc20_balance
from sybil_engine.domain.balance.tokens import Erc20Token

from web3_wizzard_lib.core.contract.velocore_lens import VelocoreLensContract
from web3_wizzard_lib.core.contract.velocore_pool import VelocorePoolContract
from web3_wizzard_lib.core.modules.liquidity.pool import Pool


class VelocorePool(Pool):
    module_name = 'VELOCORE_LIQUIDITY'
    pool_contract = 'VELOCORE_POOL'
    pool_lens_contract = 'VELOCORE_LENS'

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.chain_instance = chain_instance
        self.velocore_pool = VelocorePoolContract(self.velocore_pool_contract_address, self.web3)
        self.velocore_lens = VelocoreLensContract('0xaA18cDb16a4DD88a59f4c2f45b5c91d009549e06', self.web3)

    def deposit(self, amount_interval, account, token, min_native_balance, chain):
        if token == 'ETH':
            amount = interval_to_eth_balance(amount_interval, account, chain, self.web3)

            if amount_interval == 'all_balance':
                amount = amount.minus(min_native_balance)
        else:
            amount = interval_to_erc20_balance(amount_interval, account, token, chain, self.web3)

            erc20_token = Erc20Token(self.chain_instance['chain'], "wstETH", self.web3)

            if erc20_token.allowance(account, self.velocore_pool.contract_address) < amount.wei:
                erc20_token.approve(account, self.velocore_pool.contract_address)

        pool_address = '0x2BD146e7d95cea62C89fcCA8E529e06EEc1b053C'

        logger.info(f"Deposit {amount}")

        self.velocore_pool.deposit(account, int(amount.wei * 0.99), token, pool_address)

    def withdraw(self, account, token, chain):
        pool_address = '0x2BD146e7d95cea62C89fcCA8E529e06EEc1b053C'

        gauge = self.velocore_lens.query_gauge(pool_address, account)

        usdc_eth_vlp = gauge[14]
        eth = gauge[9]

        logger.info(f"Withdraw {eth / 10 ** 18} ETH")

        if eth / 10 ** 18 < 0.0005:
            logger.info("Withdraw amount less than 0.0005, skip")
            return

        self.velocore_pool.withdraw(account, eth, usdc_eth_vlp, pool_address)
