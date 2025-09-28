from web3_wizzard_lib.core.sybil_engine.contract import Contract
from web3_wizzard_lib.core.sybil_engine.contract.transaction_executor import evm_transaction
from web3_wizzard_lib.core.sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/nomis_attest.json")


class NomisAttestContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def attest(self,
               account,
               schema,
               expirationTime,
               revocable,
               tokenId,
               updated,
               value,
               chainId,
               calcModel,
               validationPayload
        ):
        txn_params = self.build_generic_data(account.address, False)
        txn_params['gasPrice'] = int(self.web3.eth.gas_price * 2)
        return self.contract.functions.attestNomisScoreSimple(
            schema,
            expirationTime,
            revocable,
            tokenId,
            updated,
            value,
            chainId,
            calcModel,
            validationPayload
        ).build_transaction(txn_params)

