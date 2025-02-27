from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.module.module import Module
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.gmx_reward_router import GmxRewardRouter


class GMXRewardRouter(Module):
    module_name = 'GMX_REWARD_ROUTER'
    module_config = None

    def execute(self, account, chain='ARBITRUM'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, None)

        contract_address = get_contracts_for_chain(chain_instance['chain'])['GMX_REWARD_ROUTER']
        gmx_reward_router = GmxRewardRouter(contract_address, web3)

        token = Erc20Token(chain, '0x1aDDD80E6039594eE970E5872D247bf0414C8903', web3)
        gmx_reward_router.unstake_and_redeem(account, token.balance(account).wei)

    def log(self):
        return "GMX REWARD WITHDRAW"
