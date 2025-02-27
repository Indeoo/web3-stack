from functools import wraps

from loguru import logger
from web3 import Web3

from sybil_engine.domain.balance.balance_utils import from_wei_to_eth
from sybil_engine.utils.fee_storage import add_fee
from sybil_engine.utils.gas_utils import l1_gas_price, check_gas_price
from sybil_engine.utils.tx_utils import wait_for_transaction
from sybil_engine.utils.utils import randomized_sleeping, deprecated, TransactionExecutionException


def evm_transaction(func):
    @wraps(func)
    def wrapper(instance, account, *args):
        chain_instance = instance.chain_instance
        web3 = instance.web3
        args = instance, account, *args

        return execute_transaction_internal(func, args, chain_instance, account, web3)

    return wrapper


@deprecated
def execute_transaction(func, args, chain_instance, account, web3=None):
    return execute_transaction_internal(func, args, chain_instance, account, web3)


@l1_gas_price
def execute_transaction_internal(func, args, chain_instance, account, web3=None):
    if web3 is None:
        web3 = func.__self__.web3

    check_gas_price(web3, chain_instance['gas_price_gwei'], 'L2')

    try:
        contract_txn = func(*args)

        if 'gas' not in contract_txn:
            contract_txn['gas'] = web3.eth.estimate_gas(contract_txn)

        signed_txn = account.sign_transaction(contract_txn, private_key=account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        randomized_sleeping(chain_instance['transaction_sleep_interval'])
        wait_for_transaction(tx_hash, web3)

        logger.info(f">>> {chain_instance['scan']}/tx/{Web3.to_hex(tx_hash)}")
        tx_receipt = web3.eth.get_transaction_receipt(tx_hash)

        transaction_status = tx_receipt['status']
        if transaction_status == 0:
            raise TransactionExecutionException("Transaction status is 0.")
    except Exception as e:
        raise TransactionExecutionException(f"Transaction failed in {func}.") from e

    transaction_price_wei = tx_receipt['gasUsed'] * tx_receipt['effectiveGasPrice']
    logger.info(f"Transaction fee: {from_wei_to_eth(transaction_price_wei)} {chain_instance['gas_token']}")

    add_fee(chain_instance['gas_token'], transaction_price_wei)

    return tx_hash


def evm_starknet_transaction(func):
    @wraps(func)
    def wrapper(instance, account, *args):
        chain_instance = instance.chain_instance
        web3 = instance.web3
        args = instance, account, *args

        return execute_starknet_bridge_transaction_internal(func, args, chain_instance, account, web3)

    return wrapper


def execute_starknet_bridge_transaction_internal(account, args, chain_instance, func, web3):
    tx_hash = execute_transaction_internal(func, args, chain_instance, account, web3)

    logger.info(f'>>> https://starkscan.co/contract/{account.starknet_address}#token-transfers')

    return tx_hash


def l0_evm_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        evm_decorated_func = evm_transaction(func)
        tx_hash = evm_decorated_func(*args, **kwargs)

        logger.info(f'>>> https://layerzeroscan.com/tx/{Web3.to_hex(tx_hash)}')

        return tx_hash

    return wrapper
