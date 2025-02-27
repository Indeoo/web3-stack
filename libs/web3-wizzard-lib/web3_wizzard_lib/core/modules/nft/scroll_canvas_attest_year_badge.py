import requests
from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class ScrollCanvas1YearBadge(NftSubmodule):
    module_name = 'SCROLL_CANVAS_YEAR_BADGE'
    nft_address = '0x3dacAd961e5e2de850F5E027c70b56b5Afa5DfeD'

    def execute(self, account: AppAccount, chain='SCROLL', wei_cost=from_eth_to_wei(0)):
        url = f"https://canvas.scroll.cat/badge/claim?badge={self.nft_address}&recipient={account.address}"

        proxy = {
            'http': account.proxy,
            'https': account.proxy
        }

        result = requests.get(url, proxies=proxy).json()

        Send(
            None,
            self.create_web3(account, chain)
        ).send_to_wallet(
            account,
            result['tx']['to'],
            NativeBalance(wei_cost, chain, "ETH"),
            result['tx']['data']
        )

    def log(self):
        return "SCROLL CANVAS (1 YEAR BADGE)"
