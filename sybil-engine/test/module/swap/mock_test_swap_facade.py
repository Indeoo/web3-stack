from sybil_engine.domain.swap_facade import SwapFacade
from test.module.swap.mock_dex import MockFailDex


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
