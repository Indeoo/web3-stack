import random
from hashlib import sha256

from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.module.module import Order, RepeatableModule
from sybil_engine.utils.utils import interval_to_int
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.dmail_send_mail import DmailSend


class Dmail(RepeatableModule):
    module_name = 'DMAIL'
    module_config = 'send_dmail_config'
    allowed_chains = ['ZKSYNC', 'LINEA', 'SCROLL', 'MANTA', 'BASE']
    random_order = Order.RANDOM
    repeat_conf = 'email_amount'

    @RepeatableModule.repeatable_log
    def execute(self, chain, account):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        dmail_contract_address = get_contracts_for_chain(chain)["DMAIL"]

        email = sha256(str(1e11 * random.random()).encode()).hexdigest()
        theme = sha256(str(1e11 * random.random()).encode()).hexdigest()

        args = [account, email, theme]

        dmail_sender = self.get_contract_class()(dmail_contract_address, web3)

        dmail_sender.send_mail(*args)

    def log(self):
        return "SEND EMAIL"

    def get_contract_class(self):
        return DmailSend

    def parse_params(self, module_params):
        self.validate_supported_chain(module_params['chain'])

        return (module_params['chain'],)

    def order(self):
        return Order.RANDOM

    def repeats(self, module_params):
        if self.repeat_conf not in module_params:
            return 1
        else:
            return range(interval_to_int(module_params[self.repeat_conf]))
