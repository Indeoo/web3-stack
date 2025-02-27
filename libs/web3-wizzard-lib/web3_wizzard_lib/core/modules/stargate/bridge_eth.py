from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.domain.balance.balance import NotEnoughNativeBalance
from sybil_engine.domain.balance.balance_utils import from_wei_to_eth, from_eth_to_wei
from sybil_engine.utils.utils import interval_to_round

from web3_wizzard_lib.core.contract.stargate_router_eth import StargateRouterEth
from web3_wizzard_lib.core.modules.stargate.stargate_gas_checker import get_native_fee_balance


def bridge_eth(native_without_min, account, bridge_amount_interval, from_chain_instance, to_chain_instance, web3):
    contracts = get_contracts_for_chain(from_chain_instance['chain'])

    native_fee = get_native_fee_balance(
        'ETH',
        native_without_min,
        from_chain_instance,
        to_chain_instance,
        account,
        web3
    )

    if native_fee.wei > native_without_min.wei:
        raise NotEnoughNativeBalance(
            f"Native balance ({native_without_min}) "
            f"in {native_without_min.chain} is lower than required fee ({native_fee}",
            from_chain_instance['chain']
        )

    if bridge_amount_interval == 'all_balance':
        value_wei = native_without_min.wei

        if value_wei < 0:
            raise Exception('Not enough balance')

        amount_to_bridge_wei = value_wei - native_fee.wei
        amount_to_bridge_eth = from_wei_to_eth(amount_to_bridge_wei)
    else:
        amount_to_bridge_eth = interval_to_round(bridge_amount_interval)
        amount_to_bridge_wei = from_eth_to_wei(amount_to_bridge_eth)

        value_wei = amount_to_bridge_wei + native_fee.wei

    value_wei = value_wei
    value_eth = from_wei_to_eth(value_wei)

    if value_wei > native_without_min.wei:
        raise NotEnoughNativeBalance(
            f"The account balance ({native_without_min}) < bridging amount ({value_eth}{native_without_min.token}).")

    logger.info(f"Bridging: {amount_to_bridge_eth} {native_without_min.token}")
    logger.info(f"Trying to bridge with value: {value_eth}{native_without_min.token}")

    stargate_router_eth_address = contracts["STARGATE_ROUTER_ETH"]
    stargate_router = StargateRouterEth(stargate_router_eth_address, web3)

    args = [account, value_wei, amount_to_bridge_wei, to_chain_instance]

    stargate_router.swap_eth(*args)
