from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3
from web3 import Web3

from web3_wizzard_lib.core.contract.octomos import OctomosContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class Octomos(SubModule):
    module_name = 'OCTOMOS'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['OCTOMOS']

        octomos_contract = OctomosContract(contract_address, web3)

        octomos_contract.launchpadBuy(
            account,
            Web3.to_bytes(hexstr='0x0c21cfbb').ljust(4, b'\0'),
            Web3.to_bytes(hexstr='0x53b93973').ljust(4, b'\0'),
            0,
            1,
            [],
            b''
        )

    def log(self):
        return "OCTOMOS"
