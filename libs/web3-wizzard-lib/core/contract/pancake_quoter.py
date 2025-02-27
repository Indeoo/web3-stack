from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/pancake/quoter.json")


class PancakeQuoter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def quote_exact_input_single(self, from_token: str, to_token: str, amount: int):
        return self.contract.functions.quoteExactInputSingle(
            (
                from_token,
                to_token,
                amount,
                500,
                0
            )
        ).call()[0]
