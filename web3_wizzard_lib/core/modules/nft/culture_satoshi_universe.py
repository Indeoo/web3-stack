from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaCultureWeek2Day1(NftSubmodule):
    module_name = 'LINEA_CULTURE_2_1'
    nft_address = '0xc0A2a606913A49a0B0a02F682C833EFF3829B4bA'

    def execute(self, account: AppAccount, chain='LINEA', wei_cost=0):
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
        return "LINEA CULTURE 2 WEEK DAY 1 (SATOSHI UNIVERSE)"
