import secrets

import base58
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.imagine_contract import ImagineContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class Imagine(SubModule):
    module_name = 'IMAGINE'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['IMAGINE']
        imagine_contract = ImagineContract(contract_address, web3)

        random_bytes = secrets.token_bytes(32)

        # Encode the byte string using base58
        base58_string = base58.b58encode(random_bytes).decode('utf-8')

        uri = f"https://ipfs.io/ipfs/{base58_string}/metadata.json"

        imagine_contract.mint(account, uri)

    def log(self):
        return "IMAGINE NFT"
