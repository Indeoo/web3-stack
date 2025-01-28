from loguru import logger
#from pyuseragents import random as random_ua
from requests import Session
from sybil_engine.utils.retry import retry


class IntractAPI:
    def __init__(self, account):
        self.account = account
        self.session = Session()
        self.session.headers['user-agent'] = random_ua()
        if account.proxy is not None and account.proxy != '':
            self.session.proxies.update({'http': account.proxy, 'https': account.proxy})
        else:
            logger.warning('You are not using proxy')

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def intract_get_nonce(self, address: str):
        payload = {'walletAddress': address}
        url = 'https://api.intract.io/api/qv1/auth/generate-nonce'

        self.session.headers.clear()
        r = self.session.post(url, json=payload)

        if r.json().get('success') == True:
            return r.json()['data']['nonce']
        else:
            logger.debug(f'nonce intract response: {r.status_code} {r.reason} | {r.text}')
            raise Exception(f'Couldnt generate nonce for Intract')

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def intract_login(self, address: str, signature: str):
        payload = {
            "signature": signature,
            "userAddress": address,
            "chain": {"id": 59144, "name": "Linea", "network": "Linea",
                      "nativeCurrency": {"decimals": 18, "name": "Ether", "symbol": "ETH"},
                      "rpcUrls": {"public": {"http": ["https://linea.drpc.org"]}, "default": {
                          "http": ["https://linea-mainnet.infura.io/v3/bfc263a4f3cf49998641d16c24fd0b46"]}},
                      "blockExplorers": {"etherscan": {"name": "Lineascan", "url": "https://lineascan.build/"},
                                         "default": {"name": "Lineascan", "url": "https://lineascan.build/"}},
                      "unsupported": False},
            "isTaskLogin": False,
            "width": "590px",
            "reAuth": False,
            "connector": "metamask",
            "referralCode": None,
            "referralLink": None,
            "referralSource": None
        }
        url = 'https://api.intract.io/api/qv1/auth/wallet'

        r = self.session.post(url, json=payload)

        if r.json().get('isEVMLoggedIn') == True:
            self.user_id = self.get_user()['_id']

            self.session.headers.update({
                'Cookies': r.headers["Set-Cookie"].split(';')[0],
                'Questuserid': self.user_id,
            })
            return True
        else:
            logger.debug(f'login intract response: {r.status_code} {r.reason} | {r.text}')
            raise Exception(f'Couldnt login Intract')

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def intract_get_tasks(self, compaignID):
        self.active_tasks = []

        url = f'https://api.intract.io/api/qv1/campaign/{compaignID}'
        r = self.session.get(url)

        wave = r.json()
        # for wave in r.json():
        if wave["status"] == 'ACTIVE' and wave.get('locked') != True: self.active_tasks.append(wave["name"])

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def set_wallet(self, address: str):
        try:
            if self.get_user().get('lineaWalletAddress'):
                return True

            payload = {
                "userId": self.user_id,
                "lineaWalletAddress": address
            }
            url = 'https://api.intract.io/api/qv1/linea/user/set-wallet'
            r = self.session.post(url, json=payload)

            if r.json().get('message') == "Linea wallet address updated successfully":
                logger.info(f'Wallet successfully linked')
                return True
        except Exception as err:
            raise Exception(f'Couldnt set wallet: {err} | {r.text}')

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def intract_streak(self):
        try:
            url = 'https://api.intract.io/api/qv1/linea/user/streak'
            r = self.session.post(url, json={})

            streakCount = r.json().get('streakCount')
            isFirstTimeMarked = r.json().get('isFirstTimeMarked')

            if streakCount:
                logger.info(f'New GM streak: {streakCount + 1}')
            elif isFirstTimeMarked:
                logger.info(f'New GM streak: 1')
            elif 'Linea streak already done for today' in r.text:
                logger.info(f'New GM streak: already did streak today')
            else:
                raise Exception(f'bad response {r.status_code} {r.reason}')
        except Exception as err:
            if 'Internal server error' in r.text:
                logger.error(f'Couldnt use GM streak')
            else:
                logger.error(f'Couldnt post streak: {err} | {r.text}')

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def get_user(self):
        try:
            url = 'https://api.intract.io/api/qv1/auth/get-user?projectId=660c1fa77851c55d93a1c0e0'
            r = self.session.get(url)
            return r.json()

        except Exception as err:
            raise Exception(f'Couldnt get user: {err} | {r.text}')

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def get_super_user(self):
        try:
            # self.intract_streak()

            url = 'https://api.intract.io/api/qv1/auth/get-super-user'
            r = self.session.get(url)

            return {
                'achieves': len(r.json().get('badges')),
                'streak': r.json().get('gmStreak')['streakCount'],
                'gems': r.json().get('totalGems'),
                'xp': r.json().get('totalXp'),
                'super_user_id': r.json().get('_id'),
            }

        except Exception as err:
            raise Exception(f'Couldnt get super user: {err} | {r.text}')

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def claim_achievements(self):
        try:
            url = 'https://api.intract.io/api/qv1/achievement/init'
            r = self.session.post(url)

            for achieve in r.json():
                if achieve["isClaimed"] == False and achieve["isCompleted"] == True:
                    try:
                        payload = {
                            "achievementIds": [achieve["achievementId"]]
                        }
                        url = 'https://api.intract.io/api/qv1/achievement/claim'
                        r = self.session.post(url, json=payload)

                        if 'User achievement reward already claimed' in r.text or 'User achievement not found' in r.text:
                            pass
                        else:
                            logger.info(f'Claimed achievement: {r.json()[0]["name"]}')
                    except Exception as err:
                        logger.error(
                            f'Claim achievement {achieve["achievementId"]} {achieve["name"]} error: {err} | {r.text}')

        except Exception as err:
            logger.error(f'Couldnt fetch achievements: {err} | {r.text}')

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def activate_journey(self, campaign_id: str):
        url = f'https://api.intract.io/api/qv1/journey/fetch?campaignId={campaign_id}&channelCode=DEFAULT&referralCode=null'

        r = self.session.get(url)
        if r.json().get('isActive') != True:
            logger.error(f'Activate journey error: {r.text}')

        return r.json()

    @retry(max_attempts=10, retry_interval={'from': 10, 'to': 20})
    def verify_quest(self, task):
        data = {
            "campaignId": task['campaignId'],
            "userInputs": {},
            "userVerificationData": {},
            "taskId": task['_id']
        }

        headers = {
            'questuserid': self.session.headers['Questuserid'],
            'authorization': f'Bearer {self.session.headers["Cookies"].split('=')[1]}'
        }

        url = 'https://api.intract.io/api/qv1/task/verify-v2'
        r = self.session.post(url, json=data, headers=headers)

        logger.info(r.json())

        if r.json()['verified'] == 'False':
            raise Exception("Quest wasn't verified")

        return r.status_code

    def set_primary_task_identity(self, account):
        url = 'https://api.intract.io/api/qv1/auth/set-primary-task-identity'
        payload = {"identity": account.address, "namespaceTag": "EVM"}
        r = self.session.post(url, json=payload)
