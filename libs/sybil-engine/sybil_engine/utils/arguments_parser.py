import argparse
import os
import sys


def parse_arguments(default_password, spreadsheet_id, default_module):
    parser = argparse.ArgumentParser(description='Process arguments.')

    data_folder = 'data'
    wallets_folder = f'{data_folder}/wallets'

    parser.add_argument('--profile', type=str, required=False,
                        default=os.environ.get('PROFILE', 'default'),
                        help='a string to be processed')
    parser.add_argument('--wallets', type=str, required=False,
                        default=os.environ.get('WALLETS', wallets_folder),
                        help='a string to be processed')
    parser.add_argument('--private_keys', type=str, required=False,
                        default=os.environ.get('PRIVATE_KEYS', f'{wallets_folder}/private_keys.txt'),
                        help='a string to be processed')
    parser.add_argument('--cex_addresses', type=str, required=False,
                        default=os.environ.get('CEX_ADDRESSES', f'{wallets_folder}/cex_addresses.txt'),
                        help='a string to be processed')
    parser.add_argument('--starknet_addresses', type=str, required=False,
                        default=os.environ.get('STARKNET_ADDRESSES', f'{wallets_folder}/starknet_addresses.txt'),
                        help='a string to be processed')
    parser.add_argument('--account_csv', type=str, required=False,
                        default=os.environ.get('ACCOUNT_CSV', f'{wallets_folder}/accounts.csv'),
                        help='a string to be processed')
    parser.add_argument('--proxy_file', type=str, required=False,
                        default=os.environ.get('PROXY_FILE', f'{wallets_folder}/proxy.txt'),
                        help='a string to be processed')
    parser.add_argument('--password', type=str, required=False, default=os.environ.get('PASSWORD', default_password),
                        help='a string to be processed')
    parser.add_argument('--network', type=str, required=False, default=os.environ.get('NETWORK', 'MAIN'),
                        help='a string to be processed')
    parser.add_argument('--module', type=str, required=False, default=os.environ.get('MODULE', default_module),
                        help='a string to be processed')
    parser.add_argument('--cex_conf', type=str, required=False, default=os.environ.get('CEX_CONF', 'cex'),
                        help='a string to be processed')
    parser.add_argument('--spreadsheet_id', type=str, required=False,
                        default=os.environ.get('SPREADSHEET_ID', spreadsheet_id),
                        help='a string to be processed')

    args = parser.parse_args()

    if '--private_keys' not in sys.argv:
        args.private_keys = os.path.join(args.wallets, 'private_keys.txt')
    if '--cex_addresses' not in sys.argv:
        args.cex_addresses = os.path.join(args.wallets, 'cex_addresses.txt')
    if '--starknet_addresses' not in sys.argv:
        args.starknet_addresses = os.path.join(args.wallets, 'starknet_addresses.txt')
    if '--proxy_file' not in sys.argv:
        args.proxy_file = os.path.join(args.wallets, 'proxy.txt')
    if '--account_csv' not in sys.argv:
        args.account_csv = os.path.join(args.wallets, 'accounts.csv')

    return args


def parse_profile():
    parser = argparse.ArgumentParser(description='Process arguments.')

    parser.add_argument('--profile', type=str, required=False,
                        default=os.environ.get('PROFILE', 'default'),
                        help='a string to be processed')

    args, unknown = parser.parse_known_args()
    return args
