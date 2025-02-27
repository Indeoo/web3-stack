import os
import random
import time
import traceback

from loguru import logger
from tqdm import tqdm


def int_to_decimal(qty, decimal):
    return int(qty * int("".join(["1"] + ["0"] * decimal)))


def randomized_sleeping(sleep_interval):
    x = random.randint(sleep_interval['from'], sleep_interval['to'])

    if x == 0:
        return

    for _ in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)


def interval_to_int(interval):
    return int(random.randint(interval['from'], interval['to']))


def interval_to_round(interval):
    return round(random.uniform(interval['from'], interval['to']), 6)


def deprecated(func):
    def new_func(*args, **kwargs):
        logger.warning(f"Call to deprecated function {func.__name__}", category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)

    return new_func


def print_exception_chain(exception):
    current_exception = exception
    chain_index = 1

    while current_exception:
        exception_type = type(current_exception).__name__
        exception_message = str(current_exception)

        # Extract traceback details
        tb = traceback.extract_tb(current_exception.__traceback__)
        last_call_stack = tb[-1] if tb else None  # Get the last call stack
        file_path = last_call_stack.filename if last_call_stack else 'Unknown file'
        filename = os.path.basename(file_path)  # Get only the file name, not the full path
        lineno = last_call_stack.lineno if last_call_stack else 'Unknown line'
        func_name = last_call_stack.name if last_call_stack else 'Unknown function'

        logger.error(
            f"[{chain_index}][{exception_type}]: {exception_message} ({filename}:{lineno} in {func_name}) ({file_path})")

        current_exception = current_exception.__cause__
        chain_index += 1


class AppException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AccountException(AppException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ConfigurationException(AppException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ModuleException(AppException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SwapException(AppException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class RetryException(AppException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TransactionExecutionException(AppException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
