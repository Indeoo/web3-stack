from urllib.parse import urlparse

from loguru import logger
from sybil_engine.module.module import Module
import requests


class AdsImportProxy(Module):
    module_name = 'ADS_IMPORT_PROXY'
    module_config = 'ads_import_config'

    def execute(self, ads_url, account):
        parsed_proxy = urlparse(account.proxy)
        proxy_type = parsed_proxy.scheme
        proxy_host = parsed_proxy.hostname
        proxy_port = parsed_proxy.port
        proxy_user = parsed_proxy.username
        proxy_password = parsed_proxy.password

        logger.info(f"Import proxy {account.proxy} for account {account.app_id}")

        response = requests.get(f"{ads_url}/list", params={"serial_number": str(account.app_id)})
        user_id = response.json()['data']['list'][0]["user_id"]

        self.updateProfile(ads_url, user_id, proxy_host, proxy_password, proxy_port, proxy_type, proxy_user)

    def updateProfile(self, ads_url, user_id, proxy_host, proxy_password, proxy_port, proxy_type, proxy_user):
        data = {
            "user_id": user_id,
            "user_proxy_config": {
                "proxy_type": proxy_type,
                "proxy_host": proxy_host,
                "proxy_port": str(proxy_port),
                "proxy_user": proxy_user,
                "proxy_password": proxy_password,
                "proxy_soft": "luminati"
            }
        }
        response = requests.post(f"{ads_url}/update", json=data)
        logger.info(response.status_code)
        logger.info(response.json())

    def log(self):
        return "ADS IMPORT PROXY"

    def parse_params(self, module_params):
        if 'ads_url' not in module_params:
            module_params['ads_url'] = "http://local.adspower.net:50325/api/v1/user"

        return [
            module_params['ads_url']
        ]
