from sybil_engine.utils.retry import retry


@retry(max_attempts=3, retry_interval={'from': 60 * 1, 'to': 60 * 4})
def wait_for_transaction(tx_hash, web3):
    web3.eth.wait_for_transaction_receipt(tx_hash)
