from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction, l0_evm_transaction

from web3_wizzard_lib.core.modules.stargate.stargate_gas_checker import stargate_check_gas

with open("resources/abi/stargate_router.json") as f:
    abi = f.read()


class StargateRouter(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def add_liquidity(self, account, pool_amount):
        from_address = account.address

        txn_params = self.build_generic_data(from_address, False)

        contract_txn = self.contract.functions.addLiquidity(
            self.chain_instance['stargate_usdc_pool'],
            pool_amount.wei,
            from_address
        ).build_transaction(txn_params)

        contract_txn['gas'] = (self.web3.eth.estimate_gas(contract_txn) * 1.1)

        return contract_txn

    @evm_transaction
    def instant_redeem(self, account, amount_to_bridge, stargate_pool_id):
        from_address = account.address

        txn_params = self.build_generic_data(from_address, False)

        contract_txn = self.contract.functions.instantRedeemLocal(
            stargate_pool_id,
            amount_to_bridge,
            from_address
        ).build_transaction(txn_params)
        contract_txn['gas'] = int(self.web3.eth.estimate_gas(contract_txn) * 1.1)

        return contract_txn

    @stargate_check_gas("USDC")
    @l0_evm_transaction
    def swap(self, account, value_fee, amount_to_bridge, to_chain_instance):
        from_address = account.address

        txn_params = self.build_generic_data(from_address, False)
        txn_params['value'] = value_fee

        lz_tx_obj = [0, 0, '0x0000000000000000000000000000000000000001']

        if amount_to_bridge.token == 'USDC':
            stargate_pool = to_chain_instance['stargate_usdc_pool']
        else:
            stargate_pool = to_chain_instance['stargate_eth_pool']

        contract_txn = self.contract.functions.swap(
            to_chain_instance['stargate_chain_id'],
            stargate_pool,
            stargate_pool,
            from_address,
            amount_to_bridge.wei,
            int(amount_to_bridge.wei * 0.985),
            lz_tx_obj,
            from_address,
            '0x'
        ).build_transaction(txn_params)
        contract_txn['gas'] = int(self.web3.eth.estimate_gas(contract_txn) * 1.1)

        return contract_txn

    def count_native_fee_stargate(self, chain_id, address):
        return int(
            self.contract.functions.quoteLayerZeroFee(
                chain_id,
                1,
                address,
                '0x',
                (0, 0, address)
            ).call()[0] * 1.1
        )
