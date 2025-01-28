import random
import string

import requests
from loguru import logger
from sybil_engine.domain.balance.balance_utils import from_eth_to_wei
from sybil_engine.utils.app_account_utils import AppAccount

from web3_wizzard_lib.core.contract.scroll_canvas_mint_contract import ScrollCanvasMintContract
from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class ScrollCanvasMint(NftSubmodule):
    module_name = 'SCROLL_CANVAS_MINT'
    nft_address = '0xB23AF8707c442f59BDfC368612Bd8DbCca8a7a5a'

    def execute(self, account: AppAccount, wei_cost=from_eth_to_wei(0.0005), chain='SCROLL'):
        contract = ScrollCanvasMintContract(
            '0xB23AF8707c442f59BDfC368612Bd8DbCca8a7a5a',
            self.create_web3(account, chain)
        )

        username = self.generate_username(random.randint(8, 12))
        referral = random.choice(self.get_referrals())

        logger.info(f"Mint Scroll Canvas with username {username} using ref {referral}")

        contract.mint(
            account,
            username,
            requests.get(f'https://canvas.scroll.cat/code/{referral}/sig/{account.address}').json()['signature'],
            wei_cost
        )

    def log(self):
        return "SCROLL CANVAS MINT"

    def generate_username(self, length):
        # Combine uppercase, lowercase letters and digits
        characters = string.ascii_letters + string.digits
        # Generate random string
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    def get_referrals(self):
        return [
            'POPNK',
            'GTNPB',
            'KZFXI',
            'MFWQ7'
        ]
