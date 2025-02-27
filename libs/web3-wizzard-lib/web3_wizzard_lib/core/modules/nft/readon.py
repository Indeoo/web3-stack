import random

from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.readon_contract import ReadOnContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class ReadOn(SubModule):
    module_name = 'READON'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['READON']
        readon_curate = ReadOnContract(contract_address, web3)

        low = 1700890697805328281
        high = 1709890697805328281

        # Generate a random number within the given range
        contentUrl = format(random.randint(low, high), 'x').zfill(64)

        readon_curate.curate(account, contentUrl)

    def log(self):
        return "READON NFT"
