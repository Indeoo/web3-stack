from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.balance import Erc20Balance, NativeBalance

from web3_wizzard_lib.core.contract.stargate_token_pool import StargateTokenPool


class StargatePoolToken:
    def __init__(self, chain, token, web3):
        self.chain = chain
        self.token = token
        self.web3 = web3
        self.token_pool_contract = StargateTokenPool(get_tokens_for_chain(self.chain)[self.token], self.web3)

    def balance(self, account):
        if self.token == 'STARGATE_USDC_POOL':
            return Erc20Balance(self.token_pool_contract.balance_of(account), self.chain, self.token)
        else:
            return NativeBalance(self.token_pool_contract.balance_of(account), self.chain, self.token)

    def approve(self, account, contract_on_approve):
        return self.token_pool_contract.approve(account, contract_on_approve)

    def allowance(self, account, allowance_contract):
        return self.token_pool_contract.allowance(account, allowance_contract)

