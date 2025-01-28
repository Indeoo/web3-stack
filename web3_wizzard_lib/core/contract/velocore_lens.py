from sybil_engine.contract.contract import Contract
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/velocore_lens.json")


def to_bytes32(address):
    return Web3.to_bytes(hexstr=address).rjust(32, b'\0')


class VelocoreLensContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def getPoolBalance(self):
        token_identifier = '0xe2c67A9B15e9E7FF8A9Cb0dFb8feE5609923E5DB'

        # 0x000000000000000000000000e2c67A9B15e9E7FF8A9Cb0dFb8feE5609923E5DB

        return (self.contract.functions.getPoolBalance(
            '0xe2c67A9B15e9E7FF8A9Cb0dFb8feE5609923E5DB',
            Web3.to_bytes(hexstr='0x000000000000000000000000b98308D11E2B578858Fbe65b793e71C7a0CAa43e')
        )
                .call())

    def userBalances(self):
        token_identifier = '0xe2c67A9B15e9E7FF8A9Cb0dFb8feE5609923E5DB'

        # 0x000000000000000000000000e2c67A9B15e9E7FF8A9Cb0dFb8feE5609923E5DB
        # 0x000000000000000000000000e2c67A9B15e9E7FF8A9Cb0dFb8feE5609923E5DB

        return (self.contract.functions.userBalances(
            '0xe2c67A9B15e9E7FF8A9Cb0dFb8feE5609923E5DB',
            [Web3.to_bytes(hexstr='0x000000000000000000000000b98308D11E2B578858Fbe65b793e71C7a0CAa43e')]
        )
                .call())

    def query_gauge(self, pool_address, account):
        return (self.contract.functions.queryGauge(
            pool_address,
            account.address
        )
                .call())
