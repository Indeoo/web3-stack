from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaCultureWeek4Day2Approve(NftSubmodule):
    module_name = 'LINEA_CULTURE_4_2_APPROVE'
    nft_address = '0x3f0A935c8f3Eb7F9112b54bD3b7fd19237E441Ee'

    def execute(self, account: AppAccount, chain='LINEA', wei_cost=from_eth_to_wei(0)):
        data = f"0xa22cb4650000000000000000000000000cab6977a9c70e04458b740476b498b2140196410000000000000000000000000000000000000000000000000000000000000001"

        Send(
            None,
            self.create_web3(account, chain)
        ).send_to_wallet(
            account,
            self.nft_address,
            NativeBalance(wei_cost, chain, "ETH"),
            data
        )

    def log(self):
        return "LINEA CULTURE 4 WEEK DAY 2 (Borja Moskv APPROVE)"
