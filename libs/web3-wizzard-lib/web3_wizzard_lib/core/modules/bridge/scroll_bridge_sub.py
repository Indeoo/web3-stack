from sybil_engine.utils.utils import ConfigurationException

from web3_wizzard_lib.core.modules.bridge.bridge import Bridge
from sybil_engine.data.contracts import get_contracts_for_chain
from sybil_engine.data.networks import get_chain_instance
from sybil_engine.domain.balance.balance import NotEnoughNativeBalance
from sybil_engine.domain.balance.balance_utils import interval_to_native_balance, verify_balance

from sybil_engine.utils.web3_utils import init_web3

from web3_wizzard_lib.core.contract.eth_scroll_bridge_contract import EthScrollBridgeContract
from web3_wizzard_lib.core.contract.scroll_bridge_contract import ScrollBridgeContract
from web3_wizzard_lib.core.contract.scroll_oracle import ScrollOracle

class ScrollBridgeSubModule(Bridge):

    def execute(self, bridge_amount_interval, from_chain, to_chain, token, min_native_balance, account):
        from_chain_instance = get_chain_instance(from_chain)
        web3 = init_web3(from_chain_instance, account.proxy)
        native_without_min = verify_balance(min_native_balance, from_chain_instance, account, web3)
        amount = interval_to_native_balance(bridge_amount_interval, account, from_chain_instance['chain'], web3)
        if amount.wei > native_without_min.wei:
            if bridge_amount_interval == 'all_balance':
                amount = native_without_min
            else:
                raise NotEnoughNativeBalance(
                    f"The account balance ({native_without_min}) < bridging amount ({amount}).")
        if from_chain == 'ETH_MAINNET':
            contract_oracle = get_contracts_for_chain(from_chain)["SCROLL_ORACLE"]
            fee = ScrollOracle(contract_oracle, web3).estimateCrossDomainMessageFee()

            scroll_bridge_contract_address = get_contracts_for_chain(from_chain)["SCROLL_BRIDGE"]
            scroll_bridge = EthScrollBridgeContract(scroll_bridge_contract_address, web3)

            scroll_bridge.sendMessage(account, amount.wei, fee)
        elif from_chain == 'SCROLL':
            scroll_bridge_contract_address = get_contracts_for_chain(from_chain)["SCROLL_BRIDGE"]
            scroll_bridge = ScrollBridgeContract(scroll_bridge_contract_address, web3)

            scroll_bridge.withdraw(account, amount.wei)
        else:
            raise ConfigurationException(f"{from_chain} chain is unsupported, only ETH_MAINNET and SCROLL allowed")