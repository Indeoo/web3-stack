from loguru import logger
from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/nomis.json")


class NomisContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def set_score(self,
                  account,
                  signature,
                  mintedScore,
                  calculationModel,
                  deadline,
                  metadataUrl,
                  chainId,
                  referralCode,
                  referrerCode,
                  onftMetadataUrl
                  ):
        txn_params = self.build_generic_data(account.address, False)
        txn_params['value'] = Web3.to_wei(0.001, 'ether')
        return self.contract.functions.setScore(
            signature,
            mintedScore,
            calculationModel,
            deadline,
            metadataUrl,
            chainId,
            referralCode,
            referrerCode,
            onftMetadataUrl
        ).build_transaction(txn_params)

