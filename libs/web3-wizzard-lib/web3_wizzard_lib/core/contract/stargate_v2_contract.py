from web3_wizzard_lib.core.sybil_engine.contract import Contract
from web3_wizzard_lib.core.sybil_engine.contract.transaction_executor import evm_transaction
from web3_wizzard_lib.core.sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/stargate_v2.json")


class StargateV2Contract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def send(
            self,
            account,
            value,
            send_params,
            stargate_fee,
            refund_address
    ):
        sender = account.address

        txn_params = self.build_generic_data(sender, set_contract_address=False)
        txn_params['value'] = value

        return self.contract.functions.send(
            send_params,
            stargate_fee,
            refund_address
        ).build_transaction(txn_params)

    def quote_send(self, send_params):
        return self.contract.functions.quoteSend(
            send_params,
            False
        ).call()
