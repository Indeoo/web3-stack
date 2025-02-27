from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/gmx_reward_router.json")


class GmxRewardRouter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def unstake_and_redeem(self, account, glp_amount):
        txn_params = self.build_generic_data(account.address, False)

        contract_txn = self.contract.functions.unstakeAndRedeemGlpETH(
            glp_amount,
            0,
            account.address,
        ).build_transaction(txn_params)

        return contract_txn
