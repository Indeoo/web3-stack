import time

from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

from web3_wizzard_lib.core.modules.stargate.stargate_balance_utils import NativeBalance, Erc20Balance

abi = load_abi("resources/abi/pancake/router.json")


class PancakeRouter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def swap_to_token(self, account, amount: NativeBalance, from_token: str, to_token: str, min_amount_out: int):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = amount.wei

        deadline = int(time.time()) + 1000000

        transaction_data = self.contract.encode_abi(
            "exactInputSingle",
            args=[(
                from_token,
                to_token,
                500,
                account.address,
                amount.wei,
                min_amount_out,
                0
            )]
        )

        return self.contract.functions.multicall(deadline, [transaction_data]).build_transaction(txn_params)

    @evm_transaction
    def swap_to_eth(self, account, amount: Erc20Balance, from_token: str, to_token: str, min_amount_out: int):
        txn_params = self.build_generic_data(account.address, False)

        deadline = int(time.time()) + 1000000

        transaction_data = self.contract.encode_abi(
            fn_name="exactInputSingle",
            args=[(
                from_token,
                to_token,
                500,
                "0x0000000000000000000000000000000000000002",
                amount.wei,
                min_amount_out,
                0
            )]
        )

        unwrap_data = self.contract.encode_abi(
            fn_name="unwrapWETH9",
            args=[
                min_amount_out,
                account.address
            ]

        )

        contract_txn = self.contract.functions.multicall(
            deadline,
            [transaction_data, unwrap_data]
        ).build_transaction(txn_params)

        return contract_txn
