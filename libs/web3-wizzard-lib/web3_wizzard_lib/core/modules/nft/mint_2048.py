import secrets

from sybil_engine.contract.send import Send
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.utils.sub_module import SubModule


class Mint2048(SubModule):
    module_name = '2048'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['2048']

        data = f'0x36ab86c4{secrets.token_hex(32)}0000000000000000000000000000000000000000000000000000000000000001'
        send = Send(None, web3)
        send.send_to_wallet(
            account, contract_address, NativeBalance(0, chain, "ETH"), data
        )

    def log(self):
        return "2048 NFT"
