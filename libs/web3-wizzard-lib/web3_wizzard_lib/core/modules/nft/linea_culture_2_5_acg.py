from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaCultureWeek2Day2(NftSubmodule):
    module_name = 'LINEA_CULTURE_2_5'
    nft_address = '0x057b0080120D89aE21cC622db34f2d9Ae9fF2BDE'

    def execute(self, account: AppAccount, chain='LINEA', wei_cost=from_eth_to_wei(0.0001)):
        Send(
            None,
            self.create_web3(account, chain)
        ).send_to_wallet(
            account,
            self.nft_address,
            NativeBalance(wei_cost, chain, "ETH"),
            "0x1249c58b"
        )

    def log(self):
        return "LINEA CULTURE 2 WEEK DAY 5 (ACG)"
