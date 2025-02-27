from sybil_engine.module.module import Module, Order

from web3_wizzard_lib.core.modules.stargate.bridge import StargateBridge


class StargateBridgeModule(Module):
    module_name = 'STARGATE_CLASSIC_BRIDGE'
    module_config = 'stargate_classic_config'
    random_order = Order.STRICT

    def execute(self, bridge_amount_interval, bridge_token, retry_interval, from_chain, to_chain, account):
        StargateBridge(retry_interval).bridge(
            self.min_native_balance,
            account,
            bridge_amount_interval,
            bridge_token,
            from_chain,
            to_chain
        )

    def log(self):
        return "STARGATE CLASSIC"

    def parse_params(self, module_params):
        if 'retry_interval' not in module_params:
            module_params['retry_interval'] = {'from': 60 * 5, 'to': 60 * 10}

        return (
            module_params['bridge_amount_interval'],
            module_params['bridge_token'],
            module_params['retry_interval'],
            module_params['from_chain'],
            module_params['to_chain']
        )
