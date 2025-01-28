from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction

from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/eralend.json")


class EraLendContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def mint(self, account, amount: int):
        sender = account.address

        txn_params = self.build_generic_data(sender)
        txn_params['data'] = 0x1249c58b
        txn_params['gas'] = int(self.web3.eth.estimate_gas(txn_params))

        txn_params['value'] = amount

        return txn_params

    @evm_transaction
    def redeem_underlying(self, account, amount: int):
        sender = account.address

        txn_params = self.build_generic_data(sender, False)

        return self.contract.functions.redeemUnderlying(amount).build_transaction(txn_params)

    def get_deposit_amount(self, account):
        return self.contract.functions.balanceOfUnderlying(account.address).call()
