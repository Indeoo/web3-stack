from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.data.networks import get_ids_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/layerbank.json")


class LayerBankContract(Contract):
    def __init__(self, contract_address, web3):
        self.weth_token = get_tokens_for_chain(get_ids_chain()[web3.eth.chain_id])['WETH']
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def supply(self, account, token, amount):
        txn_params = self.build_generic_data(account.address, False)

        contract_txn = self.contract.functions.supply(token, amount).build_transaction(txn_params)

        return contract_txn

    @evm_transaction
    def enter_markets(self, account, token):
        txn_params = self.build_generic_data(account.address, False)

        return self.contract.functions.enterMarkets([token]).build_transaction(txn_params)

    @evm_transaction
    def borrow(self, account, token, amount):
        txn_params = self.build_generic_data(account.address, False)

        contract_txn = self.contract.functions.borrow(token, amount).build_transaction(txn_params)

        return contract_txn

    @evm_transaction
    def repay_borrow(self, account, token, amount):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = amount

        contract_txn = self.contract.functions.repayBorrow(token, amount).build_transaction(txn_params)

        return contract_txn

    @evm_transaction
    def redeem_token(self, account, token, amount):
        txn_params = self.build_generic_data(account.address, False)

        contract_txn = self.contract.functions.redeemUnderlying(token, amount).build_transaction(txn_params)

        return contract_txn

    def market_list_of(self, account):
        return self.contract.functions.marketListOf(account.address).call()

    def account_liquidity_of(self, account):
        return self.contract.functions.accountLiquidityOf(account.address).call()
