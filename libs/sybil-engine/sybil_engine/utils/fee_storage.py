from collections import defaultdict

from loguru import logger

from sybil_engine.domain.balance.balance_utils import from_wei_to_eth

FEE = defaultdict(int)


def add_fee(gas_token, transaction_price_wei):
    FEE[gas_token] += transaction_price_wei


def print_fee():
    converted_dict = {k: float(from_wei_to_eth(v)) for k, v in FEE.items()}
    logger.info(f"Total native fee is: {converted_dict}")
