from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaCultureWeek2Day2(NftSubmodule):
    module_name = 'LINEA_CULTURE_2_3'
    nft_address = '0xF502AA456C4ACe0D77d55Ad86436F84b088486F1'

    def execute(self, account: AppAccount, chain='LINEA', wei_cost=0):
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
        return "LINEA CULTURE 2 WEEK DAY 3 (YOOLDO)"
