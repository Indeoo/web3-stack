from sybil_engine.module.module import Module
from sybil_engine.utils.utils import ConfigurationException
from sybil_engine.utils.validation_utils import validate_amount_interval, validate_chain

from web3_wizzard_lib.core.modules.bridge.scroll_bridge_sub import ScrollBridgeSubModule


class ScrollBridgeModule(Module):
    module_name = 'SCROLL_BRIDGE'
    module_config = 'scroll_bridge'

    supported_tokens = ['NATIVE']
    supported_chains = ['ETH_MAINNET', 'SCROLL']

    def execute(self, bridge_amount_interval, from_chain, to_chain, token, account):
        ScrollBridgeSubModule().execute(
            bridge_amount_interval,
            from_chain,
            to_chain,
            token,
            self.min_native_balance,
            account
        )

    def log(self):
        return "SCROLL BRIDGE"

    def parse_params(self, module_params):
        validate_amount_interval(module_params['bridge_amount_interval'])
        validate_chain(module_params['from_chain'])

        if 'token' not in module_params:
            module_params['token'] = 'NATIVE'

        if module_params['token'] not in self.supported_tokens:
            raise ConfigurationException(
                f"{module_params['token']} not supported in scroll bridge. Supported options: {self.supported_tokens}")

        if module_params['to_chain'] not in self.supported_chains or module_params[
            'to_chain'] not in self.supported_chains:
            raise ConfigurationException(
                f"{module_params['chain']} not supported in scroll bridge. Supported options: {self.supported_chains}")

        return module_params['bridge_amount_interval'], module_params['from_chain'], module_params['to_chain'], \
            module_params['token']
