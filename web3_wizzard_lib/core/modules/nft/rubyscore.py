import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.rubyscore_contract import RubyscoreContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class Rubyscore(SubModule):
    module_name = 'RUBYSCORE'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        message = " A signature is required for authorization on the platform and does not pose a threat to users!"

        message_encoded = encode_defunct(text=message)
        signed_message = Account.sign_message(message_encoded, private_key=account.key).signature.hex()

        login_request_url = f"https://rubyscore.io/api/auth/login?signature={signed_message}&message=+A+signature+is+required+for+authorization+on+the+platform+and+does+not+pose+a+threat+to+users!&wallet={account.address}"

        login_token = requests.post(login_request_url).json()['result']['token']

        request_signature_request = "https://rubyscore.io/api/attestation/claim?project=linea"
        request_signature_response = requests.post(
            request_signature_request,
            headers={
                'Authorization': f'Bearer {login_token}'
            }
        ).json()['result']

        schemaId = request_signature_response['attestationParams']['schemaId']
        expirationDate = int(request_signature_response['attestationParams']['expirationDate'])
        signature = request_signature_response['signature']

        contract_address = get_contracts_for_chain(chain)['RUBYSCORE']
        rubyscore = RubyscoreContract(contract_address, web3)
        rubyscore.attest_rubyscore(account, signature, schemaId, expirationDate)

    def log(self):
        return "RUBYSCORE"
