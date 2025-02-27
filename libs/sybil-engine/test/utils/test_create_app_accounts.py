import unittest

from sybil_engine.utils.csv_reader import read_csv_rows

from sybil_engine.domain.balance.balance_utils import interval_to_eth_balance
from sybil_engine.utils.app_account_utils import create_app_account_with_proxies, create_app_accounts_from_table, \
    validate_cex_addresses, AppAccount
from test import test_account


class TestCreateAppAccounts(unittest.TestCase):

    def test_create_zksync(self):
        test_account = create_app_account_with_proxies(
            ['0xb98308D11E2B578858Fbe65b793e71C7a0CAa43e'],
            False,
            'password',
            ['0x7726827caac94a7f9e1b160f7ea819f172f7b6f9d2a97f992c38edeab82d4110'],
            [],
            'RANDOM',
            ['0x6317842385f344acf68561f4e65f0f39e4fb4f1ad104b92bd007361aed39d8'],
        )[0]

        zksync_min_native_balance = interval_to_eth_balance({'from': 1, 'to': 1}, test_account, None, None)

    def test_create_base_account(self):
        base_test_account = create_app_account_with_proxies(
            ['0xb98308D11E2B578858Fbe65b793e71C7a0CAa43e'],
            False,
            'password',
            ['0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'],
            [],
            'RANDOM',
            ['0x6317842385f344acf68561f4e65f0f39e4fb4f1ad104b92bd007361aed39d8'],
        )[0]

        base_min_native_balance = interval_to_eth_balance({'from': 1, 'to': 1}, base_test_account, None, None)

    def test_create_zksync_from_csv(self):
        rows = read_csv_rows('test/data/wallets/accounts.csv')

        accounts = create_app_accounts_from_table(
            rows,
            'password',
            False
        )

        self.assertEqual(
            len(accounts),
            2
        )
        print(accounts)

    def test_validate_cex_addresses(self):
        app_accounts = [
            AppAccount(1, None, test_account, '1', None, None),
            AppAccount(2, None, test_account, '2', None, None)
        ]
        cex_addresses = ['1', '2']

        validate_cex_addresses(app_accounts, cex_addresses)

    def test_validate_cex_addresses_fail(self):
        app_accounts = [
            AppAccount(1, None, test_account, '1', None, None),
            AppAccount(2, None, test_account, '2', None, None)
        ]
        cex_addresses = ['1', '3']

        with self.assertRaises(Exception):
            validate_cex_addresses(app_accounts, cex_addresses)
