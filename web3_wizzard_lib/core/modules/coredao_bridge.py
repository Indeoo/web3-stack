from sybil_engine.module.module import Order, Module

from web3_wizzard_lib.core.modules.bridge.coredao_bridge_sub import CoreDaoBridgeSubModule


class CoreDaoBridge(Module):
    module_name = 'COREDAO_BRIDGE'
    allowed_chains = ['POLYGON', 'COREDAO']
    module_config = 'coredao_bridge_config'

    def execute(self, bridge_amount_interval, from_chain, to_chain, token, account):
        CoreDaoBridgeSubModule().execute(
            bridge_amount_interval,
            from_chain,
            to_chain,
            token,
            self.min_native_balance,
            account
        )

    def log(self):
        return "COREDAO BRIDGE"

    def parse_params(self, module_params):
        self.validate_supported_chain(module_params['from_chain'])
        self.validate_supported_chain(module_params['to_chain'])

        return module_params['bridge_amount_interval'], module_params['from_chain'], module_params['to_chain'], \
            module_params['token']

    def order(self):
        return Order.RANDOM
