import requests
from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.nomis_contract import NomisContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class Nomis(SubModule):
    module_name = 'NOMIS'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['NOMIS']

        response = requests.get(f'https://bg.nomis.cc/api/proxy/linea/wallet/{account.address}/score?scoreType=0&calculationModel=14&UseTokenLists=false&nonce=0&deadline=1790647549&GetCyberConnectProtocolData=false&prepareToMint=true&MintChain=0&ShouldGetReferrerCode=false&disableProxy=true&referrerCode=nomis', timeout=10)

        signature = response.json()['data']['mintData']['signature']
        mintedScore = response.json()['data']['mintData']['mintedScore']
        deadline = response.json()['data']['mintData']['deadline']
        metadataUrl = response.json()['data']['mintData']['metadataUrl']
        chainId = response.json()['data']['mintData']['chainId']
        referralCode = response.json()['data']['mintData']['referralCode']
        referrerCode = response.json()['data']['mintData']['referrerCode']
        calculationModel = response.json()['data']['mintData']['calculationModel']
        onftMetadataUrl = response.json()['data']['mintData']['onftMetadataUrl']

        nomis_contract = NomisContract(contract_address, web3)

        if mintedScore < 3000:
            formatted_score = "{:.2f}".format(mintedScore / 100)
            logger.info(f"Minted score is  {formatted_score}, minimum 30 is required, skip account")
            return

        nomis_contract.set_score(
            account,
            signature,
            mintedScore,
            calculationModel,
            deadline,
            metadataUrl,
            chainId,
            referralCode,
            referrerCode,
            onftMetadataUrl
        )

    def log(self):
        return "NOMIS POH"


def get_attest_data_media(token_auth):
    url = 'https://mp.trustalabs.ai/accounts/attest_calldata?attest_type=media'
    headers = {'Authorization': f'TOKEN {token_auth}', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        res = [r.json()]
        if res[0]['code'] == 0:
            txn_calldata = res[0]['data']
            return txn_calldata
