from loguru import logger
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NotEnoughNativeBalance
from sybil_engine.domain.balance.balance_utils import interval_to_native_balance, verify_balance
from sybil_engine.utils.utils import ConfigurationException
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.stargate_v2_contract import StargateV2Contract
from web3_wizzard_lib.core.modules.bridge.bridge import Bridge

chain_ids = {
    'LINEA': 30183,
    'SCROLL': 30214,
    'OPTIMISM': 30111,
    'ARBITRUM': 30110,
    'BASE': 30184
}


class StargateV2SubModule(Bridge):
    supported_tokens = ['NATIVE']

    def execute(self, bridge_amount_interval, from_chain, to_chain, token, min_native_balance, account):
        if token != 'NATIVE':
            raise ConfigurationException('Currently only native token bridge is supported by Stargate V2')

        from_chain_instance = get_chain_instance(from_chain)
        web3 = init_web3(from_chain_instance, account.proxy)
        stargate_v2_contract = get_contracts_for_chain(from_chain)['STARGATE_V2']

        amount = self.__calculate_bridge_amount(
            account,
            bridge_amount_interval,
            from_chain_instance,
            min_native_balance,
            web3
        )

        logger.info(f"Bridge {from_chain} –> {to_chain} | {amount}")

        send_params = (
            chain_ids[to_chain],
            f'0x000000000000000000000000{account.address[2:]}',
            amount.wei,  # amountLD,
            int(amount.wei * 0.995),  # minAmountLd,
            b'',
            b'',
            b'\x01',
        )

        stargate_v2 = StargateV2Contract(stargate_v2_contract, web3)

        stargate_fee = stargate_v2.quote_send(send_params)

        stargate_v2.send(
            account,
            amount.wei + stargate_fee[0],
            send_params,
            stargate_fee,
            account.address
        )

    def __calculate_bridge_amount(self, account, bridge_amount_interval, from_chain_instance, min_native_balance, web3):
        native_without_min = verify_balance(min_native_balance, from_chain_instance, account, web3)

        amount = interval_to_native_balance(bridge_amount_interval, account, from_chain_instance['chain'], web3)
        if amount.wei > native_without_min.wei:
            if bridge_amount_interval == 'all_balance':
                amount = native_without_min
            else:
                raise NotEnoughNativeBalance(
                    f"The account balance ({native_without_min}) < bridging amount ({amount}).")
        return amount
