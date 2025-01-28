from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.domain.balance.balance_utils import interval_to_eth_balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.utils.retry import retry

from web3_wizzard_lib.core.contract.zerolend_liq_contract import ZeroLendLiqContract
from web3_wizzard_lib.core.modules.liquidity.pool import Pool


class ZeroLendLiquidity(Pool):
    module_name = 'ZEROLEND_LIQUIDITY'
    pool_contract = 'ZEROLEND'

    @retry(max_attempts=5, retry_interval={'from': 15 * 1, 'to': 30 * 1})
    def deposit(self, amount_interval, account, deposit_token, min_native_balance, chain):
        contract = ZeroLendLiqContract(get_contracts_for_chain(chain)['ZEROLEND'], self.web3)

        zerolend_token = Erc20Token(chain, deposit_token, self.web3)

        amount = interval_to_eth_balance(amount_interval, account, chain, self.web3)

        if zerolend_token.allowance(account, contract.contract_address) < zerolend_token.balance(account).wei:
            zerolend_token.approve(account, contract.contract_address)

        contract.create_lock(account, amount)

