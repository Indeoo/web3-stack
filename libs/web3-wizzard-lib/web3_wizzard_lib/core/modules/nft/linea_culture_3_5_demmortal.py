from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaCultureWeek3Day4(NftSubmodule):
    module_name = 'LINEA_CULTURE_3_5'
    nft_address = '0x5A77B45B6f5309b07110fe98E25A178eEe7516c1'

    def execute(self, account: AppAccount, chain='LINEA', wei_cost=from_eth_to_wei(0)):
        Send(
            None,
            self.create_web3(account, chain)
        ).send_to_wallet(
            account,
            self.nft_address,
            NativeBalance(wei_cost, chain, "ETH"),
            f"0x731133e9000000000000000000000000{account.address[2:]}0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000"
        )

    def log(self):
        return "LINEA CULTURE 3 WEEK DAY 5 (Demortal)"
