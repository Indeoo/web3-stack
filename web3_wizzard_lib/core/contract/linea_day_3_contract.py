from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/linea_day_3.json")


class LineaDay3(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    # @evm_transaction
    # def mintWithVoucher(self, account):
    #     txn_params = self.build_generic_data(account.address, False)
    #
    #     contract_txn = self.contract.functions.mintWithVoucher(
    #         (
    #             '0x0000000000000000000000000000000000000000'
    #             '0x0000000000000000000000000000000000000000',
    #             0,
    #             1,
    #             1,
    #             int(datetime.now().timestamp() + 60 * 10),
    #             0,
    #             1,
    #             '0x0000000000000000000000000000000000000000'
    #         ),
    #         '0xbb6fef09ef7f8958207a489df32fa334879b963aa975b8a62a3839e3c887d5540f05bdeba16649c507c8350a987a2556425707b6f01f4592b744d9767c0b47ca1c'
    #     ).build_transaction(txn_params)
    #
    #     return contract_txn

    @evm_transaction
    def claim(self, account):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = from_eth_to_wei(0.0000029)

        contract_txn = self.contract.functions.claim(
            account.address,  # address
            0,  # uint256
            1,  # uint256
            '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',  # address
            0,  # uint256
            (
                [],  # bytes32[] - This needs to be populated with actual data or kept as empty if applicable
                2,  # uint256
                0,  # uint256
                '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'  # address
            ),
            '0x'  # bytes - This typically represents an empty byte string or could be filled if needed
        ).build_transaction(txn_params)

        return contract_txn
