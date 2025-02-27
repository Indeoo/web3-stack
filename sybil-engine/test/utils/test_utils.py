import unittest

from sybil_engine.utils.utils import print_exception_chain


class TestUtils(unittest.TestCase):

    def test_print_exception_chain(self):
        # Example usage
        try:
            # Some code that raises an exception
            1 / 0
        except Exception as e:
            print_exception_chain(e)

