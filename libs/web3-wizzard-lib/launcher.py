import glob
import importlib
import os

import web3_wizzard_lib

from sybil_engine.module.modules import *
from loguru import logger
from sybil_engine.app import launch_with_data

from web3_wizzard_lib.core.modules.swap.swap_list import swap_facade
import importlib.util


def import_all_modules(package):
    # Get the directory path of the package
    package_dir = os.path.dirname(package.__file__)

    # Get all .py files in that directory
    python_files = glob.glob(package_dir + "/*.py")

    for file in python_files:
        # Get module name from file name by removing the extension
        module_name = os.path.basename(file)[:-3]
        # Form the absolute module path by 'package.module'
        absolute_module_name = f'{package.__name__}.{module_name}'
        # Import the module using its absolute path
        importlib.import_module(absolute_module_name)


def launch():
    import_all_modules(web3_wizzard_lib.core.modules)

    logger.info(Module.__subclasses__())

    modules_data = Modules(None, swap_facade)
    #modules_data = load_module_vars("web3-wizzard-lib.utils.modules")['modules_data']

    launch_with_data(modules_data)
