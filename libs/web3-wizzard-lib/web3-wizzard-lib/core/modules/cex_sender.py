from loguru import logger
from sybil_engine.contract.send import Send
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance_utils import interval_to_native_balance, interval_to_erc20_balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.module.module import Module
from sybil_engine.utils.accumulator import add_accumulator_native_balance
from sybil_engine.utils.retry import retry
from sybil_engine.utils.validation_utils import validate_chain, validate_amount_interval
from sybil_engine.utils.web3_utils import init_web3


class SendToCex(Module):
    module_name = 'SEND_TO_CEX'
    module_config = 'send_to_cex_config'
    supported_chains = ['USDC', 'USDT', 'ZK', 'ZRO', 'OBT']

    def execute(self, chain, send_to_cex_amount_interval, token, account):
        cex_address = account.cex_address
        chain_instance = get_chain_instance(chain)
        web3 = init_web3(chain_instance, account.proxy)

        if token == 'NATIVE':
            amount = interval_to_native_balance(send_to_cex_amount_interval, account, chain_instance['chain'], web3)

            if send_to_cex_amount_interval == 'all_balance':
                amount = amount.minus(self.min_native_balance)
        elif token in self.supported_chains:
            amount = interval_to_erc20_balance(send_to_cex_amount_interval, account, token, chain, web3)
        else:
            raise Exception(f"Token {token} not supported. Only NATIVE and USDC/USDT are supported.")

        if amount.wei == 0 :
            logger.info("Wallet is empty")
            return

        self.send_funds(account, amount, cex_address, chain, chain_instance, token, web3)

        add_accumulator_native_balance("Total sent to cex", amount.wei)

    @retry(max_attempts=5, retry_interval={'from': 60 * 2, 'to': 60 * 3})
    def send_funds(self, account, amount, cex_address, chain, chain_instance, token, web3):
        logger.info(f"Send {amount} to {cex_address} ({chain_instance['chain']})")
        if token == 'NATIVE':
            send = Send(None, web3)
            send.send_to_wallet(account, cex_address, amount)
        elif token in self.supported_chains:
            erc20_token = Erc20Token(chain, token, web3)
            erc20_token.transfer(amount, cex_address, account)
        else:
            raise Exception(f"Token {token} not supported. Only NATIVE and USDC/USDT are supported.")

    def log(self):
        return "SEND TO CEX"

    def parse_params(self, module_params):
        validate_chain(module_params['chain'])
        validate_amount_interval(module_params['amount'])

        return module_params['chain'], module_params['amount'], module_params['token']
