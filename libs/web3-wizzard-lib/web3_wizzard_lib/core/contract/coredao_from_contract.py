from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import l0_evm_transaction
from sybil_engine.utils.file_loader import load_abi

from web3_wizzard_lib.core.modules.stargate.l0_data import l0_chain_ids

abi = load_abi("resources/abi/coredao_bridge.json")


class CoreDaoFromContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @l0_evm_transaction
    def bridge(self, account, amount, token, fee, to_chain):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = fee

        contract_txn = self.contract.functions.bridge(
            token,
            l0_chain_ids[to_chain],
            amount.wei,
            account.address,
            False,
            (
                account.address,
                '0x0000000000000000000000000000000000000000'
            ),
            b''
        ).build_transaction(txn_params)

        return contract_txn

    def estimate_bridge_fee(self, to_chain):
        return self.contract.functions.estimateBridgeFee(
            l0_chain_ids[to_chain],
            False,
            b''
        ).call()[0]
