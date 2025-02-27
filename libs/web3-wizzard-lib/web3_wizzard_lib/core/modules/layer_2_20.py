import random

from loguru import logger
from sybil_engine.contract.send import Send
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import get_native_balance
from sybil_engine.module.module import Order, RepeatableModule
from sybil_engine.utils.utils import interval_to_int, ConfigurationException
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.bridge.orbiter_sub import bridge_codes


class Layer2_20(RepeatableModule):
    module_name = 'Layer2_20'
    allowed_chains = ['ZKSYNC', 'OPTIMISM', 'BASE', 'LINEA', 'ARBITRUM', 'SCROLL']
    random_order = Order.RANDOM
    repeat_conf = 'repeats'
    module_config = 'layer_2_20_config'

    @RepeatableModule.repeatable_log
    def execute(self, chains, to_chains, account):
        chain = random.choice(chains)
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        temp_to_chains = [item for item in to_chains if item != chain]
        if not temp_to_chains:
            raise ConfigurationException("No chains to send to")
        to_chain = random.choice(temp_to_chains)

        layer2_20_contract_address = get_contracts_for_chain(chain)["LAYER2_20"]

        send = Send(layer2_20_contract_address, web3)

        amount_to_send = NativeBalance(
            230000000000000 + bridge_codes[to_chain],
            chain,
            chain_instance['gas_token']
        )
        data = '0x646174613a2c7b2270223a226c61796572322d3230222c226f70223a22636c61696d222c227469636b223a22244c32222c22616d74223a2231303030227d'

        native_balance = get_native_balance(account, web3, chain_instance)

        logger.info(f"Native {chain} balance: " + str(native_balance))
        logger.info(f"Inscription {chain} -> {to_chain} | {amount_to_send}")

        send.send_to_wallet(account, layer2_20_contract_address, amount_to_send, data)

    def log(self):
        return "LAYER2_20"

    def parse_params(self, module_params):
        return module_params['chains'], module_params['to_chains']

    def order(self):
        return Order.RANDOM

    def repeats(self, module_params):
        if self.repeat_conf not in module_params:
            return 1
        else:
            return range(interval_to_int(module_params[self.repeat_conf]))
