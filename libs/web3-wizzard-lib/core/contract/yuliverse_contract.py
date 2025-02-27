from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/yoddlo.json")


class YuliverseContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def purchase(self, account):
        txn_params = self.build_generic_data(account.address, True)

        function_selector = "0x064a181e"

        # Example uint256 paramet er
        varg0 = 123456789  # Make sure this is the value you intend to use

        # Example bytes parameter (signature) - Ensure this is exactly 65 bytes
        varg1 = b'Your65ByteSignatureHere'  # This should be the actual signature bytes

        # Encoding the transaction data
        data = function_selector
        data += varg0.to_bytes(32, byteorder='big').hex()
        data += (32).to_bytes(32, byteorder='big').hex()  # Offset for dynamic data
        data += (65).to_bytes(32, byteorder='big').hex()  # Length of the signature
        data += varg1.hex()

        print(data)

        # Concatenate the selector and the encoded parameters
        txn_params['data'] = data

        return txn_params
