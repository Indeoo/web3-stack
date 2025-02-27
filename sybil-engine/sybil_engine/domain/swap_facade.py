from sybil_engine.domain.balance.tokens import Erc20Token

from sybil_engine.utils.utils import ConfigurationException


class SwapFacade:
    def __init__(self, dex_classes):
        self.dex_classes = dex_classes

    def swap(self, account, amount_to_swap, chain_instance, pair, swap_app, from_token, to_token, web3):
        slippage_coef = 1 - pair['slippage'] * 0.01

        dex = self.get_dex(swap_app, chain_instance, web3)

        from_token = Erc20Token(chain_instance['chain'], from_token, web3)
        to_token = Erc20Token(chain_instance['chain'], to_token, web3)

        dex.swap(amount_to_swap, from_token, to_token, slippage_coef, account)

    def get_dex(self, swap_app, chain_instance, web3):
        dex_class = next((dex_class for dex_class in self.get_dex_classes() if dex_class.dex_name == swap_app), None)

        if dex_class is None:
            raise ConfigurationException(f"Wrong pair.py configuration for {swap_app}")

        return dex_class(chain_instance, web3)

    def get_swap_apps(self):
        return [swap_app_name.dex_name for swap_app_name in self.get_all_swap_apps()]

    def get_swap_apps_by_chain(self, chain_name):
        filtered_apps = {swap_app for swap_app in self.get_all_swap_apps() if chain_name in swap_app.supported_chains}

        return [swap_app_name.dex_name for swap_app_name in filtered_apps]

    def get_all_swap_apps(self):
        return self.dex_classes

    def get_dex_classes(self):
        return self.dex_classes
