from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.arena_games_contract import ArenaGamesContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class ArenaGames(SubModule):
    module_name = 'ARENA_GAMES'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['ARENA_GAMES']
        arena_games_contract = ArenaGamesContract(contract_address, web3)

        arena_games_contract.safe_mint(account)

    def log(self):
        return "ARENA GAMES NFT"
