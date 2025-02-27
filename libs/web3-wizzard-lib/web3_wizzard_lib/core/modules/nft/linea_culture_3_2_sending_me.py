from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaCultureWeek3Day2(NftSubmodule):
    module_name = 'LINEA_CULTURE_3_2'
    nft_address = '0xEaea2Fa0dea2D1191a584CFBB227220822E29086'

    def execute(self, account: AppAccount, chain='LINEA', wei_cost=from_eth_to_wei(0)):
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
        return "LINEA CULTURE 3 WEEK DAY 2 (Sending Me)"
