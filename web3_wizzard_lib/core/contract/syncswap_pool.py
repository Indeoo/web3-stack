from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/syncswap_pool.json")


class SyncSwapPoolContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def get_amount_out(self, account, amount_to_swap, token_in_address):
        sender = account.address

        contract = self.web3.eth.contract(address=self.contract_address, abi=abi)

        return contract.functions.getAmountOut(token_in_address, amount_to_swap.wei, sender).call()

    def get_pool(self, from_token, to_token):
        return self.contract.functions.getPool(
            from_token,
            to_token
        ).call()

    def balanceOf(self, account):
        return self.contract.functions.balanceOf(account.address).call()