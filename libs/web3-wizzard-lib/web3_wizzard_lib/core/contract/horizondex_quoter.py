from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/horizondex_quoter.json")


class HorizonDexQuoter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def quote_exact_input_single(self, amount: int, from_token_address: str, to_token_address: str):
        return self.contract.functions.quoteExactInputSingle(
            (from_token_address, to_token_address, amount, 40, 0)
        ).call()[1]
