import random
import string

from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.kreatorland_contract import KreatorLandContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class KreatorLand(SubModule):
    module_name = 'KREATOR_LAND'

    def execute(self, account, chain='ZKSYNC'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['KREATOR_LAND']
        kreator_land_contract = KreatorLandContract(contract_address, web3)

        uri = f'https://cloudflare-ipfs.com/ipfs/{random_string}/metadata.json'

        kreator_land_contract.mint(account, uri)

    def log(self):
        return "Kreator Land"

    def parse_params(self, module_params):
        return []


def random_string(length=59):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choice(characters) for _ in range(length))
