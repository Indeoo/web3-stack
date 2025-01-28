from sybil_engine.contract.weth import WETH
from sybil_engine.data.networks import get_ids_chain
from sybil_engine.data.tokens import get_tokens_for_chain

from web3_wizzard_lib.core.contract.basiliskcontract import BasiliskContract
from web3_wizzard_lib.core.modules.bank.bank import Bank


class Basilisk(Bank):
    app_name = 'BASILISK_LANDING'
    supported_chains = ['ZKSYNC']

    def __init__(self, contract, web3):
        self.contract = BasiliskContract(contract, web3)

    def supply(self, account, amount):
        self.contract.mint(account, amount.wei)

    def redeem(self, account, withdraw):
        self.contract.redeem_underlying(account, withdraw.wei)

    def get_deposit_amount(self, account, token):
        weth_token = get_tokens_for_chain(get_ids_chain()[self.contract.web3.eth.chain_id])['BASILISK_LANDING']

        return WETH(weth_token, self.contract.web3).balance_of(account)
