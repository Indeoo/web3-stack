from sybil_engine.config.app_config import get_cex_data, get_cex_conf
from sybil_engine.domain.cex.binance import Binance
from sybil_engine.domain.cex.okx import OKX
from sybil_engine.module.module import Module
from sybil_engine.utils.app_account_utils import AppAccount
from sybil_engine.utils.utils import ConfigurationException


class CEXSubAccountTransfer(Module):
    module_name = 'CEX_SUB_ACCOUNT_TRANSFER'
    module_config = 'cex_account_transfer_config'

    def execute(self, cex, account: AppAccount):
        password, cex_data = get_cex_data()

        tokens = ['ETH', 'CORE', 'POL', 'USDC', 'USDT', 'OKB', 'ZRO']

        if cex == 'okx':
            cex_obj = OKX(cex_data[get_cex_conf()], password)
        elif cex == 'binance':
            cex_obj = Binance(cex_data[get_cex_conf()], password)
        else:
            raise ConfigurationException(f"{cex} is not")

        cex_obj.transfer_from_sub_account(tokens)

    def log(self):
        return "CEX SUB ACCOUNT TRANSFER"

    def parse_params(self, module_params):
        if 'cex' not in module_params:
            module_params['cex'] = 'okx'

        return [module_params['cex']]
