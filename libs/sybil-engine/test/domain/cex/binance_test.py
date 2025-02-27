import os
import unittest

from loguru import logger

from sybil_engine.domain.cex.binance import Binance


class TestBinance(unittest.TestCase):

    def test_binance(self):
        binance = Binance(
            os.getenv("BINANCE_API"),
            os.getenv("ENCRYPTION_PASSWORD").encode("utf-8")
        )

        logger.info(binance.get_asset_valuation())