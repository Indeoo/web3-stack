from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NotEnoughERC20Balance
from sybil_engine.domain.balance.balance_utils import interval_to_erc20_balance, get_native_balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.utils.retry import retry
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.coredao_contract import CoreDaoContract
from web3_wizzard_lib.core.contract.coredao_from_contract import CoreDaoFromContract
from web3_wizzard_lib.core.modules.bridge.bridge import Bridge


class CoreDaoBridgeSubModule(Bridge):
    supported_chains = ['POLYGON', 'COREDAO']

    @retry(max_attempts=5, retry_interval={'from': 60 * 15, 'to': 60 * 25})
    def execute(self, bridge_amount_interval, from_chain, to_chain, token, min_native_balance, account):
        chain_instance = get_chain_instance(from_chain)
        web3 = init_web3(chain_instance, account.proxy)

        erc20_token = Erc20Token(from_chain, token, web3)

        amount = interval_to_erc20_balance(bridge_amount_interval, account, token, from_chain, web3)

        logger.info(f"Native balance: {get_native_balance(account, web3, chain_instance)}")
        logger.info(f"Balance: {erc20_token.balance(account)}")

        logger.info(f"Bridge {from_chain + ' -> ' + to_chain} {amount}")

        if amount.wei == 0:
            raise NotEnoughERC20Balance(f"Can't swap zero balance")

        coredao_contract = get_contracts_for_chain(from_chain)['COREDAO_BRIDGE']

        if erc20_token.allowance(account, coredao_contract) < amount.wei:
            erc20_token.approve(account, coredao_contract)

        if from_chain == 'COREDAO':
            coredao = CoreDaoFromContract(coredao_contract, web3)
            fee = coredao.estimate_bridge_fee(to_chain)
        else:
            coredao = CoreDaoContract(coredao_contract, web3)
            fee = coredao.estimate_bridge_fee()

        coredao.bridge(account, amount, erc20_token.erc20_contract.contract_address, fee, to_chain)
