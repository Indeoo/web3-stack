import time

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/zebra.json")


class ZebraContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def get_min_amount_out(self, amount, from_token: str, to_token: str):
        min_amount_out = self.contract.functions.getAmountsOut(
            amount.wei,
            [
                Web3.to_checksum_address(from_token),
                Web3.to_checksum_address(to_token)
            ]
        ).call()
        return min_amount_out[1]

    @evm_transaction
    def swap_to_token(self, account, amount, from_token: str, to_token: str, min_amount_out: int):
        tx_data = self.build_generic_data(
            account.address,
            False
        )

        tx_data['value'] = amount.wei

        deadline = int(time.time()) + 1000000

        contract_txn = self.contract.functions.swapExactETHForTokens(
            min_amount_out,
            [
                from_token,
                to_token,
            ],
            account.address,
            deadline
        ).build_transaction(tx_data)

        return contract_txn

    @evm_transaction
    def swap_to_eth(self, account, amount, from_token: str, to_token: str, min_amount_out: int):
        tx_data = self.build_generic_data(
            account.address,
            False
        )

        deadline = int(time.time()) + 1000000

        contract_txn = self.contract.functions.swapExactTokensForETH(
            amount.wei,
            min_amount_out,
            [
                from_token,
                to_token,
            ],
            account.address,
            deadline
        ).build_transaction(tx_data)

        return contract_txn
