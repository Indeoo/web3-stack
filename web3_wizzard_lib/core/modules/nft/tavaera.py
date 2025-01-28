from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.tavaera_id import TavaeraID
from web3_wizzard_lib.core.contract.tavaera_mint import Tavaera
from web3_wizzard_lib.core.utils.sub_module import SubModule


class TavaeraModule(SubModule):
    module_name = 'TAVAERA'

    def execute(self, account, chain='ZKSYNC'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        chain_contracts = get_contracts_for_chain(chain)

        tavaera_id = TavaeraID(chain_contracts['TAVAERA_ID'], web3)
        tavaera = Tavaera(chain_contracts['TAVAERA_MINT'], web3)

        logger.info("Mint Tavaera ID")
        tavaera_id.mint_citizen_id(account)

        logger.info("Mint Tavaera NFT")
        tavaera.mint(account)

    def log(self):
        return "CREATE TAVAERA ACCOUNT"
