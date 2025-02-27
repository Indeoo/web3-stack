from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaCultureWeek2Day2(NftSubmodule):
    module_name = 'LINEA_CULTURE_2_6'
    nft_address = '0x0841479e87Ed8cC7374d3E49fF677f0e62f91fa1'

    def execute(self, account: AppAccount, chain='LINEA', wei_cost=from_eth_to_wei(0)):
        Send(
            None,
            self.create_web3(account, chain)
        ).send_to_wallet(
            account,
            self.nft_address,
            NativeBalance(wei_cost, chain, "ETH"),
            "0x00000000"
        )

    def log(self):
        return "LINEA CULTURE 2 WEEK DAY 6 (Toad The Great)"
