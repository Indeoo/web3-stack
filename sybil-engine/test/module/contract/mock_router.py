from loguru import logger

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import TransactionExecutionException
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/erc20.json")


class MockRouter(Contract):
    def __init__(self, contract_address, web3, retries, retry_counter=0):
        self.reties = retries
        self.retry_counter = retry_counter
        super().__init__(contract_address, web3, abi)

    def swap(self, account, contract):
        if self.retry_counter < self.reties:
            self.retry_counter += 1
            raise TransactionExecutionException("Error")
        else:
            logger.info("swap")

            txn_contract = {
                "chainId": self.web3.eth.chain_id,
                'from': account.address,
                'to': account.address,
                'value': 10000000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(account.address),
            }

            return txn_contract
