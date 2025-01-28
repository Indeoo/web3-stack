from sybil_engine.contract.send import Send
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.utils.sub_module import SubModule


class WizzardsOfLinea(SubModule):
    module_name = 'LINEA_CULTURE_4'

    def execute(self, account: AppAccount, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        send = Send(None, web3)
        send.send_to_wallet(
            account,
            '0xD540038B0B427238984E0341bA49F69CD80DC139',
            NativeBalance(0, chain, "ETH"),
            "0x00000000"
        )

    def log(self):
        return "WIZZARDS OF LINEA"
