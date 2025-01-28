from sybil_engine.module.module import Module
from sybil_engine.utils.utils import ConfigurationException
from sybil_engine.utils.validation_utils import validate_amount_interval, validate_chain

from web3_wizzard_lib.core.modules.bridge.orbiter_sub import OrbiterSubModule


class OrbiterModule(Module):
    module_name = 'ORBITER'
    module_config = 'orbiter_config'

    supported_tokens = ['NATIVE', 'USDC', 'USDT', 'WETH']

    def execute(self, bridge_amount_interval, from_chain, to_chain, token, account):
        OrbiterSubModule().execute(
            bridge_amount_interval,
            from_chain,
            to_chain,
            token,
            self.min_native_balance,
            account
        )

    def log(self):
        return "ORBITER BRIDGE"

    def parse_params(self, module_params):
        validate_amount_interval(module_params['bridge_amount_interval'])
        validate_chain(module_params['from_chain'])

        if 'token' not in module_params:
            module_params['token'] = 'NATIVE'

        if module_params['token'] not in self.supported_tokens:
            raise ConfigurationException(
                f"{module_params['token']} not supported in orbiter. Supported options: {self.supported_tokens}")

        return module_params['bridge_amount_interval'], module_params['from_chain'], module_params['to_chain'], \
            module_params['token']
