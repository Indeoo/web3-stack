from eth_account.messages import encode_defunct
from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.module.module import Module
from sybil_engine.utils.file_loader import load_abi
from sybil_engine.utils.utils import AccountException
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.intract.intract_api import IntractAPI
from web3_wizzard_lib.core.modules.intract.utils import TgReport, WindowName, make_text_border

VERIFY_DATA = load_abi("resources/verify_data.json")

class IntractClaim(Module):
    module_name = 'INTRACT_CLAIM'
    module_config = None

    def execute(self, task_id, account, compaign_id='66bb5618c8ff56cba848ea8f', from_chain='LINEA'):
        windowname = WindowName()

        intract_api = IntractAPI(account)
        tg_report = TgReport()
        windowname.update_accs()

        stats = {}

        web3 = init_web3(get_chain_instance(from_chain), None)

        self.authorize(intract_api, compaign_id, account, web3)

        campaign_funcs = {
            "Linea LXP Latest Rush": self.linea_lxp,
        }
        intract_api.set_primary_task_identity(account)
        intract_api.activate_journey(compaign_id)
        linea_xp = intract_api.get_user().get("totalXp") or "0"

        if task_id == 'SKIP_CHECK':
            if int(linea_xp) == 100:
                raise AccountException("Skip account tasks where already claimed")
            else:
                return

        for task in intract_api.active_tasks:
            if task in list(campaign_funcs.keys()):
                campaign_funcs[task](task, task_id, intract_api)
            else:
                logger.info(f' > Task "{task}" will appear soon...')

        account_data = intract_api.get_super_user()
        linea_xp = intract_api.get_user().get("totalXp") or "0"

        logger.info('')  # for clearly logs
        tg_report.update_logs('<i>Statistics</i>')
        logger.info('')
        text = f'Achievements: {account_data["achieves"]}\n' \
               f'GM Streak: {account_data["streak"]}\n' \
               f'Gems: {account_data["gems"]}\n' \
               f'XP: {account_data["xp"]}\n' \
               f'Linea XP: {linea_xp}'
        new_text = make_text_border(text=text)
        for string in new_text.split('\n'): logger.success(string)

        stats.update({
            'linea_xp': linea_xp,
            'xp': account_data["xp"],
            'gm_streak': account_data["streak"],
            'achievements': account_data["achieves"],
            'gems': account_data["gems"],
        })

    def authorize(self, browser, compaign_id, account, web3):
        nonce = browser.intract_get_nonce(address=account.address)
        text = f'Nonce: {nonce}'
        signature = f'0x{web3.eth.account.sign_message(encode_defunct(text=text), private_key=account.key).signature.hex()}'
        browser.intract_login(address=account.address, signature=signature)
        browser.intract_get_tasks(compaign_id)

        browser.set_wallet(address=account.address)
        #browser.claim_achievements()

    def linea_lxp(self, task_name: str, task_id, intract_api, week=0):
        logger.info(f' > Completing "{task_name}"...')

        for task in VERIFY_DATA['campaigns'][str(week)]['quest']['tasks']:
            if task_id is not None:
                if task['_id'] == task_id:
                    intract_api.verify_quest(task)
            else:
                intract_api.verify_quest(task)

    def log(self):
        return "INTRACT CLAIM"

    def parse_params(self, module_params):
        if 'taskID' not in module_params:
            module_params['taskID'] = None

        return [
            module_params['taskID']
        ]
