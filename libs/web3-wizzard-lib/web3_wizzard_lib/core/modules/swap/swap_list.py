from web3_wizzard_lib.core.domain.dex import Dex
from web3_wizzard_lib.core.domain.swap_facade import SwapFacade
from web3_wizzard_lib.core.sybil_engine.utils.package_import_utils import get_all_subclasses, import_all_modules_in_directory


def get_swap_classes():
    import_all_modules_in_directory("web3_wizzard_lib.core.modules.swap")
    return get_all_subclasses(Dex)

swap_facade = SwapFacade(get_swap_classes())
