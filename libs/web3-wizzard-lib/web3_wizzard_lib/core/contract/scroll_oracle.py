from web3_wizzard_lib.core.sybil_engine.contract import Contract
from web3_wizzard_lib.core.sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/scroll_oracle.json")

class ScrollOracle(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def estimateCrossDomainMessageFee(self):
        return self.contract.functions.estimateCrossDomainMessageFee(168000).call()
