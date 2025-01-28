import random

from loguru import logger
from sybil_engine.contract.erc20contract import Erc20Contract
from sybil_engine.contract.send import Send
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.data.tokens import get_tokens_for_chain
from sybil_engine.domain.balance.balance import NotEnoughNativeBalance
from sybil_engine.domain.balance.balance_utils import interval_to_erc20_balance, \
    interval_to_native_balance, verify_balance
from sybil_engine.utils.utils import ConfigurationException
from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.orbiter_starknet import OrbiterStarknet
from web3_wizzard_lib.core.modules.bridge.bridge import Bridge

bridge_codes = {
    "ETH": 9001,
    "ARBITRUM": 9002,
    "POLYGON": 9006,
    "OPTIMISM": 9007,
    "BSC": 9015,
    "ARBITRUM_NOVA": 9016,
    "ZKSYNC": 9014,
    "POLYGON_ZK": 9017,
    "BASE": 9021,
    "LINEA": 9023,
    "SCROLL": 9019,
    #"X_LAYER": 9027, DONT USE
    "ZORA": 9030,
    "MANTA": 9031,
    "ZKFAIR": 9038
}


class OrbiterSubModule(Bridge):
    supported_tokens = ['NATIVE', 'USDC', 'USDT', 'WETH']

    def execute(self, bridge_amount_interval, from_chain, to_chain, token, min_native_balance, account):
        from_chain_instance = get_chain_instance(from_chain)
        web3 = init_web3(from_chain_instance, account.proxy)

        if isinstance(to_chain, list):
            to_chain = random.choice(to_chain)
        if to_chain not in bridge_codes:
            raise ConfigurationException(f"{to_chain} not supported in orbiter")

        amount = self.__calculate_bridge_amount(account, bridge_amount_interval, from_chain_instance, to_chain, token,
                                                min_native_balance, web3)

        logger.info(f"Bridge {from_chain} –> {to_chain} | {amount}")
        self.__perform_bridge(account, amount, from_chain, to_chain, token, web3)

    def __perform_bridge(self, account, amount, from_chain, to_chain, token, web3):
        if token == 'NATIVE':
            self.__bridge_native(account, amount, from_chain, to_chain, web3)
        else:
            self.__bridge_token(account, amount, from_chain, web3)

    def __calculate_bridge_amount(self, account, bridge_amount_interval, from_chain_instance, to_chain, token,
                                  min_native_balance, web3):
        if token == 'NATIVE':
            native_without_min = verify_balance(min_native_balance, from_chain_instance, account, web3)

            amount = interval_to_native_balance(bridge_amount_interval, account, from_chain_instance['chain'], web3)
            if amount.wei > native_without_min.wei:
                if bridge_amount_interval == 'all_balance':
                    amount = native_without_min
                else:
                    raise NotEnoughNativeBalance(
                        f"The account balance ({native_without_min}) < bridging amount ({amount}).")
        else:
            amount = interval_to_erc20_balance(bridge_amount_interval, account, token, from_chain_instance['chain'],
                                               web3)
            if bridge_amount_interval == 'all_balance':
                amount.wei = amount.wei - 10 ** 5

        amount.wei = self.__adjust_amount_by_bridge_code(amount.wei, to_chain)

        return amount

    def __adjust_amount_by_bridge_code(self, wei_amount, to_chain):
        bridge_code = bridge_codes.get(to_chain)
        if not bridge_code:
            raise ConfigurationException(f"No bridge code found for {to_chain}")
        return int(f"{wei_amount // 10 ** 4}{bridge_code}")

    def __bridge_native(self, account, amount, from_chain, to_chain, web3):
        if to_chain == 'STARKNET':
            if amount.readable() <= 0.0065 or amount.readable() >= 5:
                raise NotEnoughNativeBalance(f"Limit range amount for starknet 0.0065 – 5 ETH | {amount}")

            if from_chain != 'ZKSYNC':
                raise ConfigurationException("only ZKSYNC can bridge to STARKNET")

            orbiter_wallet = get_contracts_for_chain(from_chain)['ORBITER_STARKNET']
            orbiter_starknet = OrbiterStarknet(orbiter_wallet, web3)
            orbiter_starknet.bridge(account, amount)
        else:
            orbiter_wallet = get_contracts_for_chain(from_chain)['ORBITER']
            send = Send(orbiter_wallet, web3)
            send.send_to_wallet(account, orbiter_wallet, amount)

    def __bridge_token(self, account, amount, from_chain, web3):
        contracts = get_contracts_for_chain(from_chain)

        if 'ORBITER_ERC20' not in contracts:
            raise ConfigurationException(f"ERC20 is not supported for {from_chain}")

        erc20 = Erc20Contract(get_tokens_for_chain(from_chain)[amount.token], web3)
        erc20.transfer(account, amount, contracts['ORBITER_ERC20'])
