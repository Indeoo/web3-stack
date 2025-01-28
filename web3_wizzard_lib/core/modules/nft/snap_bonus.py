from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.snap_contract import SnapContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class SnapBonus(SubModule):
    module_name = 'SNAP_BONUS'
    allow_reuse_address = True

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['SNAP']
        social_scan = SnapContract(contract_address, web3)

        balance = social_scan.contract.functions.balanceOf(account.address).call()
        token_id = social_scan.contract.functions.tokenOfOwnerByIndex(account.address, 0).call()

        if balance == 0:
            logger.error(f"[{account.app_id}][{account.address}] Not found NFT. Skip module")
            return

        social_scan.stake(account, token_id)

    def log(self):
        return "SNAP_BONUS MINT NFT"
