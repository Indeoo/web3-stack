from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi
from eth_abi import encode

abi = load_abi("resources/abi/frog_war_contract.json")


class FrogWarContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def claim(self, account):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = 100000000000000

        return self.contract.functions.claim(
            account.address,
            1,
            1,
            '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
            100000000000000,
            (
                ['0x0000000000000000000000000000000000000000000000000000000000000000'],
                # Note the brackets indicating an array
                1,
                0,
                '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
            ),
            '0x'
        ).build_transaction(txn_params)

    @evm_transaction
    def claim_bonus(self, account):
        txn_params = self.build_generic_data(account.address, False)

        _receiver = account.address
        _tokenId = 6
        _quantity = 1
        _currency = '0x21d624c846725ABe1e1e7d662E9fB274999009Aa'
        _pricePerToken = 0

        return self.contract.functions.claim(
            _receiver, _tokenId, _quantity, _currency, _pricePerToken,
            [[encode(['bytes32'], [b''])], 1, _pricePerToken, _currency], b''
        ).build_transaction(txn_params)
