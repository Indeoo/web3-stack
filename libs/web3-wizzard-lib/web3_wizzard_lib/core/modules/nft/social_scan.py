from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.social_scan_contract import SocialScanContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class SocialScan(SubModule):
    module_name = 'SOCIAL_SCAN'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['SOCIAL_SCAN']
        social_scan = SocialScanContract(contract_address, web3)

        social_scan.set_approval_for_all(account, '0x0caB6977a9c70E04458b740476B498B214019641', True)

    def log(self):
        return "SOCIAL SCAN NFT"
