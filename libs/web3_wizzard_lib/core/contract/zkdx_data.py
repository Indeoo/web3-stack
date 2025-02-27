from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/zkdx_data.json")


class ZKDXDataContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)
        # self.zkdx_token = '0x176211869cA2b568f2A7D4EE941E073a821EE1ff'
        self.zkdx_token = '0x2167C4D5FE05A1250588F0B8AA83A599e7732eae'

    def get_balance(self, account):
        return self.contract.functions.getTokenBalances(account.address, [self.zkdx_token]).call()
