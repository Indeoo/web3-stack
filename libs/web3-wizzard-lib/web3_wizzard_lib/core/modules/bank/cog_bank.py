from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.utils.utils import ConfigurationException

from web3_wizzard_lib.core.contract.cog_erc20 import CogErc20Contract
from web3_wizzard_lib.core.modules.bank.bank import Bank


class Cog(Bank):
    app_name = 'COG_USDC'
    supported_chains = ['SCROLL']

    def __init__(self, chain, web3):
        self.contract_address = get_contracts_for_chain(chain)[self.app_name]
        self.contract = CogErc20Contract(self.contract_address, web3)

    def supply(self, account, amount):
        raise ConfigurationException("Only redeem supported for Compound V3")

    def redeem(self, account, amount, token):
        self.contract.redeem(account, amount)

    def get_deposit_amount(self, account, token):
        return self.contract.balance_of(account)
