from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/basiliks.json")


class BasiliskContract(Contract):

    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def get_deposit_amount(self, account):
        return self.contract.functions.balanceOfUnderlying(account.address).call()

    @evm_transaction
    def mint(self, account, amount_wei):
        tx_data = self.build_generic_data(account.address)

        tx_data['data'] = self.contract.encode_abi('mint', args=())
        tx_data['gas'] = int(self.web3.eth.estimate_gas(tx_data) * 1.1)

        tx_data.update({"value": amount_wei})

        return tx_data

    @evm_transaction
    def redeem_underlying(self, account, amount):
        tx_data = self.build_generic_data(account.address, False)

        return self.contract.functions.redeemUnderlying(amount).build_transaction(tx_data)

    # @evm_transaction
    # def enable_collateral(self):
    #     logger.info(f"[{self.account_id}][{self.address}] Enable collateral on basilisk.py")
    #
    #     contract = self.get_contract(BASILISK_CONTRACTS["collateral"], BASILISK_ABI)
    #
    #     tx_data = await self.get_tx_data()
    #
    #     transaction = await contract.functions.enterMarkets(
    #         [Web3.to_checksum_address(BASILISK_CONTRACTS["landing"])]
    #     ).build_transaction(tx_data)
    #
    #     return transaction
    #
    # @evm_transaction
    # def disable_collateral(self):
    #     logger.info(f"[{self.account_id}][{self.address}] Disable collateral on basilisk.py")
    #
    #     contract = self.get_contract(BASILISK_CONTRACTS["collateral"], BASILISK_ABI)
    #
    #     tx_data = await self.get_tx_data()
    #     transaction = await contract.functions.exitMarket(
    #         Web3.to_checksum_address(BASILISK_CONTRACTS["landing"])
    #     ).build_transaction(tx_data)
    #
    #     return transaction
