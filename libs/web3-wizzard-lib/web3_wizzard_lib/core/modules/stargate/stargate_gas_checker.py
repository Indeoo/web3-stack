import functools

from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.domain.balance.balance import NativeBalance, NotEnoughNativeBalance
from sybil_engine.domain.balance.balance_utils import get_native_balance, from_eth_to_wei
from sybil_engine.utils.l0_utils import L0FeeToHigh
from sybil_engine.utils.utils import randomized_sleeping


def stargate_check_gas(token):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args):
            check_gas(token, self.chain_instance, args[-1], args[0], self.web3)
            return func(self, *args)

        return wrapper

    return decorator


def check_gas(token, chain_instance, to_chain_instance, account, web3):
    while True:
        try:
            verify_stargate_fee(token, chain_instance, to_chain_instance, account, web3)
            return
        except L0FeeToHigh as e:
            logger.info(e)
            randomized_sleeping({'from': 60 * 4, 'to': 60 * 8})
        except Exception as e:
            raise StargateBridgeException("Stargate bridge error") from e


def verify_stargate_fee(token, from_chain_instance, to_chain_instance, account, web3):
    native_balance = get_native_balance(account, web3, from_chain_instance)
    native_fee_balance = get_native_fee_balance(token, native_balance, from_chain_instance, to_chain_instance, account,
                                                web3)

    logger.info(f"Native LayerZero fee: {native_fee_balance.log_line()}")
    if native_fee_balance.wei > native_balance.wei:
        raise NotEnoughNativeBalance(
            f"Native balance ({native_balance.log_line()}) < Native LayerZero required fee")
    if native_fee_balance.wei > from_eth_to_wei(from_chain_instance['max_l0_fee']):
        raise L0FeeToHigh(f"Native LayerZero fee is to high")


def get_native_fee_balance(token, native_balance, from_chain_instance, to_chain_instance, account, web3):
    chain_contracts = get_contracts_for_chain(from_chain_instance['chain'])

    if token in ['ETH', 'USDC']:
        from web3_wizzard_lib.core.contract.stargate_router import StargateRouter
        stargate_router = StargateRouter(chain_contracts["STARGATE_ROUTER"], web3)

        wei_balance = stargate_router.count_native_fee_stargate(
            to_chain_instance['stargate_chain_id'],
            account.address
        )
    else:
        raise Exception("Token not supported")

    return NativeBalance(wei_balance, native_balance.chain, native_balance.token)


class StargateBridgeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
