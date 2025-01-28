import requests
from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.utils.retry import retry
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.nomis_attest_contract import NomisAttestContract
from web3_wizzard_lib.core.utils.sub_module import SubModule


class NomisAttest(SubModule):
    module_name = 'NOMIS_ATTEST'

    def execute(self, account, chain='LINEA'):
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        contract_address = get_contracts_for_chain(chain)['NOMIS_ATTEST']

        url_template = f'http://nomis.cc/api/proxy/verax/attestation-data?address={account.address}&nonce=0'

        response = self.get_attest(url_template)

        mintedScore = response['data']['value']

        if mintedScore < 3000:
            formatted_score = "{:.2f}".format(mintedScore / 100)
            logger.info(f"Minted score is  {formatted_score}, minimum 30 is required, skip account")
            return

        schema = response['data']['schema']
        expirationTime = response['data']['expirationTime']
        revocable = response['data']['revocable']
        tokenId = response['data']['tokenId']
        updated = response['data']['updated']
        value = response['data']['value']
        chainId = response['data']['chainId']
        calcModel = response['data']['calcModel']
        validationPayload = response['data']['validationPayload']

        nomis_attest_contract = NomisAttestContract(contract_address, web3)

        nomis_attest_contract.attest(
            account,
            schema,
            expirationTime,
            revocable,
            tokenId,
            updated,
            value,
            chainId,
            calcModel,
            validationPayload
        )

    @retry(max_attempts=15, retry_interval={'from': 60 * 1, 'to': 60 * 4})
    def get_attest(self, url_template):
        response = requests.get(url_template)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"HTTP error {response.json()}")

    def log(self):
        return "ATTEST NOMIS SCORE"
