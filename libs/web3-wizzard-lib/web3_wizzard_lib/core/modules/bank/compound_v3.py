from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_ids_chain
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.utils.utils import ConfigurationException

from web3_wizzard_lib.core.contract.compound_v3 import CompoundV3Contract
from web3_wizzard_lib.core.contract.compund_v3_bulker import CompoundV3BulkerContract
from web3_wizzard_lib.core.modules.bank.bank import Bank


class CompoundV3(Bank):
    app_name = 'COMPOUND_V3'
    supported_chains = ['SCROLL']

    def __init__(self, chain, web3):
        compound_v3_address = get_contracts_for_chain(chain)[self.app_name]
        self.contract = CompoundV3Contract(compound_v3_address, web3)
        compound_v3_bulker_address = get_contracts_for_chain(chain)['COMPOUND_V3_BULKER']
        self.contract_bulker = CompoundV3BulkerContract(compound_v3_bulker_address, web3)

    def supply(self, account, amount):
        raise ConfigurationException("Only redeem supported for Compound V3")

    def get_repay_borrow_amount(self, account):
        return self.contract.borrow_balance_of(account)

    def repay_borrow(self, account, amount):
        erc20_token = Erc20Token(self.contract.chain_instance['chain'], "USDC", self.contract.web3)

        if erc20_token.allowance(account, self.contract.contract_address) < 100:
            erc20_token.approve(account, self.contract.contract_address)

        return self.contract.supply(account, amount, erc20_token.erc20_contract.contract_address)

    def redeem(self, account, amount, token):
        actions = '0x414354494f4e5f57495448445241575f4e41544956455f544f4b454e00000000'
        self.contract_bulker.invoke(account, amount, actions)

    def get_deposit_amount(self, account, token):
        token_address = get_tokens_for_chain(get_ids_chain()[self.contract.web3.eth.chain_id])[token]
        compound_v3_address = get_contracts_for_chain(get_ids_chain()[self.contract.web3.eth.chain_id])[self.app_name]

        return CompoundV3Contract(compound_v3_address, self.contract.web3).user_collateral(
            account,
            token_address
        )
