from loguru import logger
from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/nidus.json")


class NidumContract(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def mint_nft(self, account, claim_data):
        txn_params = self.build_generic_data(account.address, False)

        token_ids = [9]
        nft_amounts = [1]
        nonce = 0

        message = claim_data['message']
        signature = claim_data['signature']

        return self.contract.functions.mintFromShadowBatch(
            _tokenID=token_ids,
            _nftAmountForMint=nft_amounts,
            _nonce=nonce,
            _msgForSign=message,  # The original hashed message (no changes needed here)
            _signature=signature  # The generated signature
        ).build_transaction(txn_params)

    @evm_transaction
    def burn(self, account):
        txn_params = self.build_generic_data(account.address, False)
        token_id = 9

        balance = self.contract.functions.balanceOf(account.address, token_id).call()
        if balance == 0:
            logger.error(f"[{account.app_id}][{account.address}] No nidum nft. Mint first. Skip module")
            return

        return self.contract.functions.burn(
            self.contract.address, 9, 1
        ).build_transaction(txn_params)
