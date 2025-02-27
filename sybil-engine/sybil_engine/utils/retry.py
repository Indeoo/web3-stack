import functools

from loguru import logger

from sybil_engine.utils.utils import print_exception_chain, randomized_sleeping, SwapException, \
    TransactionExecutionException


def retry(max_attempts=3, retry_interval={'from': 60 * 5, 'to': 60 * 10}, expected_exception=Exception,
          throw_exception=Exception):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except expected_exception as e:
                    attempts = handle(attempts, max_attempts, e, retry_interval, throw_exception, func)

        return wrapper

    return decorator


def retry_self(max_attempts=3, expected_exception=TransactionExecutionException, throw_exception=SwapException):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(self, *args, **kwargs)
                except expected_exception as e:
                    attempts = handle(attempts, max_attempts, e, self.retry_interval, throw_exception, func)

        return wrapper

    return decorator


def handle(attempts, max_attempts, e, retry, throw_exception, func):
    attempts += 1
    logger.error(f"Error during attempt {attempts}/{max_attempts}:")
    print_exception_chain(e)
    if attempts < max_attempts:
        randomized_sleeping(retry)
    else:
        raise throw_exception(f"Function {func.__name__} failed after {max_attempts} attempts") from e
    return attempts
