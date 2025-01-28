import random

from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.omnisea import OmniSea
from web3_wizzard_lib.core.utils.sub_module import SubModule


class OmniSeaModule(SubModule):
    module_name = 'OMNI_SEA'

    def execute(self, account, chain='ZKSYNC'):

        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['OMNISEA']
        omnisea = OmniSea(contract_address, web3)

        title, symbol = self.generate_collection_data()

        omnisea.create(account, title, symbol)

    @staticmethod
    def generate_collection_data():
        title = "".join(random.sample([chr(i) for i in range(97, 123)], random.randint(5, 15)))
        symbol = "".join(random.sample([chr(i) for i in range(65, 91)], random.randint(3, 6)))
        return title, symbol

    def log(self):
        return "OMNI SEA COLLECTION"
