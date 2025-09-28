from web3_wizzard_lib.core.domain.swap_facade import SwapFacade
from web3_wizzard_lib.tests.core.sybil_engine.module.swap.mock_dex import MockFailDex


class MockTestSwapFacade(SwapFacade):
    def __init__(self, dex_classes):
        super().__init__(dex_classes)

    def get_dex_classes(self):
        return {
            MockFailDex
        }


swap_facade = MockTestSwapFacade(
    {
        MockFailDex: ['ZKSYNC', 'LINEA']
    }
)
