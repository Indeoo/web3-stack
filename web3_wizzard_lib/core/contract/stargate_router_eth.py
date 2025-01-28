from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction, l0_evm_transaction

from web3_wizzard_lib.core.modules.stargate.stargate_gas_checker import stargate_check_gas

with open("resources/abi/stargate_swapETH_abi.json") as f:
    abi = f.read()


class StargateRouterEth(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def add_liquidity_eth(self, account, pool_amount):
        from_address = account.address

        txn_params = self.build_generic_data(from_address, False)
        txn_params['value'] = pool_amount.wei

        contract_txn = self.contract.functions.addLiquidityETH().build_transaction(txn_params)

        return contract_txn

    @stargate_check_gas(token='ETH')
    @l0_evm_transaction
    def swap_eth(self, account, value_wei, amount_to_bridge_wei, to_chain_instance):
        from_address = account.address

        txn_params = self.build_generic_data(account.address, False)
        txn_params['value'] = value_wei

        contract_txn = self.contract.functions.swapETH(
            to_chain_instance['stargate_chain_id'],
            from_address,
            from_address,
            amount_to_bridge_wei,
            int(amount_to_bridge_wei * 0.985)
        ).build_transaction(txn_params)

        return contract_txn
