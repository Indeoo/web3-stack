from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/linea_ens_names.json")


class LineaEnsNamesContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)
        self.addr_contract = web3.eth.contract(
            abi='[{"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"uint256","name":"coinType","type":"uint256"},{"internalType":"bytes","name":"a","type":"bytes"}],"name":"setAddr","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"node","type":"bytes32"},{"internalType":"address","name":"a","type":"address"}],"name":"setAddr","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
        )

    def available(self, linea_name):
        return self.contract.functions.available(linea_name).call()

    def make_commitment(self, account, linea_name, duration, secret, data):
        return self.contract.functions.makeCommitment(
            linea_name,
            account.address,
            duration,
            secret,
            "0x86c5AED9F27837074612288610fB98ccC1733126",
            [data],
            True,
            0,
        ).call().hex()

    def redeemed(self, account):
        return self.contract.functions.redeemed(account.address).call()

    @evm_transaction
    def register_poh(self, account, linea_name, duration, secret, data, poh_signature):
        txn_params = self.build_generic_data(account.address, set_contract_address=False)

        return self.contract.functions.registerPoh(
            linea_name,
            account.address,
            duration,
            secret,
            "0x86c5AED9F27837074612288610fB98ccC1733126",
            [data],
            True,
            0,
            poh_signature["sign"]
        ).build_transaction(txn_params)

    @evm_transaction
    def commit(self, account, commitment):
        txn_params = self.build_generic_data(account.address, set_contract_address=False)

        return self.contract.functions.commit(
            "0x" + commitment
        ).build_transaction(txn_params)
