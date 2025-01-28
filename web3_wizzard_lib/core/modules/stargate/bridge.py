from loguru import logger
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance_utils import verify_balance
from sybil_engine.utils.retry import retry_self
from sybil_engine.utils.utils import AccountException
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.modules.stargate.bridge_eth import bridge_eth
from web3_wizzard_lib.core.modules.stargate.bridge_tokens import bridge_usdc

MAX_ATTEMPTS = 5


class StargateBridge:
    def __init__(self, retry_interval):
        self.retry_interval = retry_interval

    def bridge(self, min_native_balance, account, bridge_amount_interval, token, from_chain, to_chain):
        from_chain_config = get_chain_instance(from_chain)
        to_chain_config = get_chain_instance(to_chain)
        web3 = init_web3(from_chain_config, account.proxy)

        logger.info(f"======= Bridging {token} {from_chain} ==> {to_chain} ::: {account.address} =======")

        self._bridge(account, bridge_amount_interval, from_chain_config, min_native_balance, to_chain_config, token,
                     web3)

    @retry_self(max_attempts=MAX_ATTEMPTS, expected_exception=Exception, throw_exception=AccountException)
    def _bridge(self, account, bridge_amount_interval, from_chain_config, min_native_balance, to_chain_config, token,
                web3):
        native_without_min = verify_balance(min_native_balance, from_chain_config, account, web3)

        if token == 'ETH':
            bridge_eth(native_without_min, account, bridge_amount_interval, from_chain_config, to_chain_config, web3)
        elif token == 'USDC':
            bridge_usdc(native_without_min, account, bridge_amount_interval, from_chain_config, to_chain_config, web3)
        else:
            raise ValueError(f"Unsupported bridge token: {token}, only ETH and USDC are supported")
