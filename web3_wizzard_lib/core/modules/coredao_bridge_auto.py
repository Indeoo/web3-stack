from sybil_engine.module.module import Order, RepeatableModule
from sybil_engine.utils.utils import interval_to_int, randomized_sleeping

from web3_wizzard_lib.core.modules.bridge.coredao_bridge_sub import CoreDaoBridgeSubModule


class CoreDaoBridgeAuto(RepeatableModule):
    module_name = 'COREDAO_BRIDGE_AUTO'
    allowed_chains = ['POLYGON', 'COREDAO']
    random_order = Order.RANDOM
    repeat_conf = 'repeats'
    module_config = 'coredao_bridge_auto_config'

    @RepeatableModule.repeatable_log
    def execute(self, from_chain, to_chain, bridge_amount_interval, token, sleep_interval, account):
        CoreDaoBridgeSubModule().execute(bridge_amount_interval, from_chain, to_chain, token, account)
        randomized_sleeping(sleep_interval)
        CoreDaoBridgeSubModule().execute(bridge_amount_interval, to_chain, from_chain, token, account)

    def log(self):
        return "COREDAO BRIDGE AUTO"

    def parse_params(self, module_params):
        return [
            module_params['from_chain'],
            module_params['to_chain'],
            module_params['bridge_amount_interval'],
            module_params['token'],
            module_params['sleep_interval'],
        ]

    def order(self):
        return Order.RANDOM

    def repeats(self, module_params):
        if self.repeat_conf not in module_params:
            return 1
        else:
            return range(interval_to_int(module_params[self.repeat_conf]))
