from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.domain.balance.balance import Erc20Balance, NotEnoughNativeBalance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.utils.web3_utils import get_amount_to_bridge_usdc

from web3_wizzard_lib.core.contract.stargate_router import StargateRouter


def bridge_usdc(native_balance, account, bridge_amount_interval, from_chain_config, to_chain_config, web3):
    if (from_chain_config['chain'] == 'FANTOM' and to_chain_config['chain'] == 'BASE') or (
            to_chain_config['chain'] == 'FANTOM' and from_chain_config['chain'] == 'BASE'):
        raise Exception('Stargate does not allow FANTOM<>BASE USDC transfer ')
    erc20_token = Erc20Token(from_chain_config['chain'], 'USDC', web3)

    token_balance = erc20_token.balance(account)

    logger.info(f"Token balance: {token_balance}")

    if token_balance.wei == 0:
        raise Exception(f"USDC balance is 0")

    amount_to_bridge = token_balance if bridge_amount_interval == 'all_balance' else Erc20Balance(
        get_amount_to_bridge_usdc(bridge_amount_interval),
        native_balance.chain,
        'USDC'
    )

    if amount_to_bridge.wei > token_balance.wei:
        raise NotEnoughNativeBalance(f"Account balance ({amount_to_bridge}) < {amount_to_bridge} amount to bridge.")

    logger.info(f"Bridging: {amount_to_bridge}")

    erc20_token = Erc20Token(from_chain_config['chain'], "USDC", web3)

    chain_contracts = get_contracts_for_chain(from_chain_config['chain'])

    stargate_router_address = chain_contracts["STARGATE_ROUTER"]

    if erc20_token.allowance(account, stargate_router_address) < amount_to_bridge.wei:
        erc20_token.allowance(account, stargate_router_address)

    stargate_router = StargateRouter(chain_contracts["STARGATE_ROUTER"], web3)
    native_fee_wei = stargate_router.count_native_fee_stargate(to_chain_config['stargate_chain_id'], account.address)

    args = [account, native_fee_wei, amount_to_bridge, to_chain_config]

    stargate_router.swap(*args)
