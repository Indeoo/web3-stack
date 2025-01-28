from sybil_engine.contract.contract import Contract
from sybil_engine.data.networks import get_ids_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/merkly.json")


class L2TelegraphMinter(Contract):
    def __init__(self, contract_address, web3):
        self.weth_token = get_tokens_for_chain(get_ids_chain()[web3.eth.chain_id])['WETH']
        super().__init__(contract_address, web3, abi)

    def mint(self, account):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = Web3.to_wei(0.0005, "ether")
        contract_txn = self.contract.functions.mint().build_transaction(txn_params)

        return contract_txn
