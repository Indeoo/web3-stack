from loguru import logger
from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/stargate_token_pool.json")

MAX_ALLOWANCE = 115792089237316195423570985008687907853269984665640564039457584007913129639935


class StargateTokenPool(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def approve_pool(self, account, contract_on_approve):
        logger.info(f"Approving token for pool")

        sender = account.address

        txn_params = self.build_generic_data(sender, set_contract_address=False)

        contract_txn = self.contract.functions.approve(
            Web3.to_checksum_address(contract_on_approve),
            MAX_ALLOWANCE
        ).build_transaction(txn_params)

        contract_txn['gas'] = int(self.web3.eth.estimate_gas(contract_txn) * 1.1)

        return contract_txn

    def balance_of(self, account):
        return self.contract.functions.balanceOf(account.address).call()

    def approve(self, account, contract_on_approve):
        logger.info(f"Approving token")

        txn_params = self.build_generic_data(account.address, False)

        return self.contract.functions.approve(
            Web3.to_checksum_address(contract_on_approve),
            MAX_ALLOWANCE
        ).build_transaction(txn_params)

    def allowance(self, account, allowance_contract):
        return self.contract.functions.allowance(account.address, Web3.to_checksum_address(allowance_contract)).call()
