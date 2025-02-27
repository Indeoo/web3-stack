from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/reactor_fusion.json")


class ReactorFusionContract(Contract):

    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    def get_deposit_amount(self, account):
        return self.contract.functions.balanceOf(account.address).call()

    @evm_transaction
    def mint(self, account, amount_wei: int):
        tx_data = self.build_generic_data(account.address)

        tx_data['data'] = self.contract.encode_abi('mint', args=())
        tx_data['gas'] = int(self.web3.eth.estimate_gas(tx_data))
        tx_data['value'] = amount_wei

        return tx_data

    @evm_transaction
    def redeem_underlying(self, account, amount):
        tx_data = self.build_generic_data(account.address, False)

        return self.contract.functions.redeem(amount).build_transaction(tx_data)

        # if amount > 0:
        #     logger.info(
        #         f"[{self.account_id}][{self.address}] Make withdraw from ReactorFusion | " +
        #         f"{Web3.from_wei(amount, 'ether')} ETH"
        #     )
        #
        #
        # else:
        #     logger.error(f"[{self.account_id}][{self.address}] Deposit not found")

    # @retry
    # @check_gas
    # async def enable_collateral(self):
    #     logger.info(f"[{self.account_id}][{self.address}] Enable collateral on ReactorFusion")
    #
    #     contract = self.get_contract(REACTORFUSION_CONTRACTS["collateral"], REACTORFUSION_ABI)
    #
    #     tx_data = await self.get_tx_data()
    #
    #     transaction = await contract.functions.enterMarkets(
    #         [Web3.to_checksum_address(REACTORFUSION_CONTRACTS["landing"])]
    #     ).build_transaction(tx_data)
    #
    #     signed_txn = await self.sign(transaction)
    #
    #     txn_hash = await self.send_raw_transaction(signed_txn)
    #
    #     await self.wait_until_tx_finished(txn_hash.hex())
    #
    # @retry
    # @check_gas
    # async def disable_collateral(self):
    #     logger.info(f"[{self.account_id}][{self.address}] Disable collateral on ReactorFusion")
    #
    #     contract = self.get_contract(REACTORFUSION_CONTRACTS["collateral"], REACTORFUSION_ABI)
    #
    #     tx_data = await self.get_tx_data()
    #
    #     transaction = await contract.functions.exitMarket(
    #         Web3.to_checksum_address(REACTORFUSION_CONTRACTS["landing"])
    #     ).build_transaction(tx_data)
    #
    #     signed_txn = await self.sign(transaction)
    #
    #     txn_hash = await self.send_raw_transaction(signed_txn)
    #
    #     await self.wait_until_tx_finished(txn_hash.hex())
