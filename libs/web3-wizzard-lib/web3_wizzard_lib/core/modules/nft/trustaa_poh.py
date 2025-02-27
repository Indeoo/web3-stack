import requests
from sybil_engine.contract.send import Send
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NativeBalance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.nft.sign import sign_in_message
from web3_wizzard_lib.core.utils.sub_module import SubModule


class TrustaPoh(SubModule):
    module_name = 'TRUSTA_POH'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['TRUSTA_POH']

        token_auth = sign_in_message(account, web3)
        txn_calldata = get_attest_data_humanity(token_auth)

        score = txn_calldata['message']['score']
        if score != -1:
            raise Exception(f'Score кошелька равен {score}, аттестация не выполняется')

        send = Send(contract_address, web3)
        send.send_to_wallet(
            account,
            contract_address,
            NativeBalance(txn_calldata['calldata']['value'], chain, 'ETH'),
            txn_calldata['calldata']['data']
        )

    def log(self):
        return "TRUSTA POH (Group A)"


def get_attest_data_humanity(token_auth):
    url = 'https://mp.trustalabs.ai/accounts/attest_calldata?attest_type=humanity'
    headers = {'Authorization': f'TOKEN {token_auth}', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        res = [r.json()]
        if res[0]['code'] == 0:
            txn_calldata = res[0]['data']
            return txn_calldata

