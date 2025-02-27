from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/dmail.json")


class DmailSend(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def send_mail(self, account, to, subject):
        sender = account.address

        txn_params = self.build_generic_data(sender, set_contract_address=False)

        return self.contract.functions.send_mail(to, subject).build_transaction(txn_params)
