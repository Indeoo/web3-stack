import requests
from loguru import logger
from sybil_engine.module.module import Module


class OrbiterChecker(Module):
    module_name = 'ORBITER_CHECKER'
    module_config = None

    total_points = 0

    def execute(self, account):
        url = f'https://api.orbiter.finance/points_platform/rank/address/{account.address.lower()}'

        response = requests.get(url)

        points = int(response.json()['result']['point'])

        if points > 0:
            self.total_points = self.total_points + points

        logger.info(f"Points {points}")
        logger.info(f"Total points {self.total_points}")

    def log(self):
        return "ORBITER CHECKER"
