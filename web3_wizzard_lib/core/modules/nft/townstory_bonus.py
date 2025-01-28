import requests
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.townstory_bonus_contract import TownstoryBonusContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class TownstoryBonus(SubModule):
    module_name = 'TOWNSTORY_BONUS'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['TOWNSTORY_BONUS']

        townstory_bonus_contract = TownstoryBonusContract(contract_address, web3)

        signature, deadline = get_travelbag_signature(account.address, account.proxy)

        townstory_bonus_contract.claim_linea_travelbag(account, signature, deadline)

    def log(self):
        return "CREATE TOWNSTORY BONUS"


def get_travelbag_signature(wallet, proxy):
    proxies = {'http': proxy,
               'https': proxy}
    url = 'https://townstory.io//api'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Content-Length": "70",
        "Accept": "*/*",
        "Origin": "https://townstory.io",
        "Referer": "https://townstory.io/linea"

    }
    data = {"action": "getLineaSign", "address": f'{wallet.lower()}'}

    r = requests.post(url, data=data, headers=headers, proxies=proxies)
    res = r.json()
    return res['signature'], res['deadline']
