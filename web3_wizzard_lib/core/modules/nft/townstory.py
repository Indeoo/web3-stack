from json import dumps
from time import time

import requests
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.townstory_contract import TownstoryContract
from web3_wizzard_lib.core.modules.nft.sign import sign_msg
from web3_wizzard_lib.core.utils.sub_module import SubModule


class Townstory(SubModule):
    module_name = 'TOWNSTORY'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['TOWNSTORY']

        message_text = get_message(account)
        message_signature = sign_msg(account, message_text, web3)
        txn_signature, deadline = get_txn_signature(account, message_signature)

        townstory_contract = TownstoryContract(contract_address, web3)

        townstory_contract.create_account_sign(account, txn_signature, deadline)

    def log(self):
        return "CREATE TOWNSTORY ACOUNT"


def get_txn_signature(account, message_signature):
    data = {"header": {"version": "1.0.1", "baseVersion": "1.0.0", "referer": ""},
            "transaction": {"func": "register.loginByWallet",
                            "params": {"hall": 0, "wallet": "metamask", "chain": "linea",
                                       "signature": message_signature, "address": account.address}}}
    json_data = dumps(data)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url1 = 'https://aws-login.townstory.io/town-login/handler.php'
    r = requests.get(url1, data=json_data, headers=headers)
    response = r.json()
    if response['result'] != 'failed':
        txn_signature = r.json()['response']['signature']
        deadline = r.json()['response']['deadline']
        return txn_signature, deadline


def get_time_nonce():
    time_nonce = int(time() / 86400)
    return time_nonce


def get_address_line(address):
    address_line = (address[:19] + '...' + address[-18:]).lower()
    return address_line


def get_message(wallet):
    nonce = get_time_nonce()
    address_line = get_address_line(wallet.address)
    message = ('Welcome to Town Story! \n\n'
               'Click to sign in and accept the Town Story\n'
               'Terms of Service:\n'
               'https://townstory.io/\n\n'
               'This request will not trigger a blockchain\n'
               'transaction or cost any gas fees.\n\n'
               'Your authentication status will reset after\n'
               'each session.\n\n'
               'Wallet address:\n'
               f'{address_line}\n\n'
               f'Nonce: {nonce}')
    return message
