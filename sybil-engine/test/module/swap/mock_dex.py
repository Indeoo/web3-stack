from sybil_engine.domain.dex import Dex
from loguru import logger

from test.module.contract.mock_router import MockRouter


class MockFailDex(Dex):
    dex_name = 'MockDex'
    swap_contract = 'USDC'

    def __init__(self, chain_instance, web3, retries, sleeping_interval={'from': 0, 'to': 0}, retry_counter=0):
        self.reties = retries
        self.retry_counter = retry_counter
        super().__init__(chain_instance, web3, sleeping_interval)
        self.success_mock_router = MockRouter(self.tokens[self.swap_contract], self.web3, retries)

    def swap_token_for_native(self, account, amount_to_swap, from_token_address, slippage):
        logger.info("swap_token_for_native")

        args = [account, '0x80115c708E12eDd42E504c1cD52Aea96C547c05c']

        func = self.success_mock_router.swap

        return args, func

    def swap_token_for_token(self, account, amount_to_swap, slippage, from_token_address, to_token_address):
        logger.info("swap_token_for_token")

        args = [account, '0x80115c708E12eDd42E504c1cD52Aea96C547c05c']

        func = self.success_mock_router.swap

        return args, func

    def swap_native_for_token(self, account, amount_to_swap, slippage, to_token_address):
        logger.info("swap_native_for_token")

        args = [account, '0x80115c708E12eDd42E504c1cD52Aea96C547c05c']

        func = self.success_mock_router.swap

        return args, func
