import unittest

from eth_account import Account
from loguru import logger

from web3_wizzard_lib.core.sybil_engine.config.app_config import set_network
from web3_wizzard_lib.core.sybil_engine.utils.app_account_utils import AppAccount
from web3_wizzard_lib.core.modules.nft.linea_wheel import LineaWheel


class LineaWheelTest(unittest.TestCase):

    def test_shouldTestLineaWheel(self):
        logger.info("Test module [LINEA_WHEEL]")

        try:
            set_network('MAIN')

            private_key = ""
            account = Account.from_key(private_key)
            app_account = AppAccount(1, None, account, None, None)
            linea_wheel = LineaWheel()

            linea_wheel.execute(app_account, 'LINEA')
        except Exception as e:
            self.fail(f"Some function raised an exception: {e}")