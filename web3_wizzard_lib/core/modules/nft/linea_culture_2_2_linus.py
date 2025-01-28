from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaCultureWeek2Day2(NftSubmodule):
    module_name = 'LINEA_CULTURE_2_2'
    nft_address = '0xBcFa22a36E555c507092FF16c1af4cB74B8514C8'

    def execute(self, account: AppAccount, chain='LINEA', wei_cost=0):
        Send(
            None,
            self.create_web3(account, chain)
        ).send_to_wallet(
            account,
            self.nft_address,
            NativeBalance(wei_cost, chain, "ETH"),
            "0x1b7af8fc0c21cfbb000000000000000000000000000000000000000000000000000000001ffca9db000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        )

    def log(self):
        return "LINEA CULTURE 2 WEEK DAY 2 (LINUS)"
