import argparse
import os
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process arguments.')

    if '--profile' in sys.argv:
        parser.add_argument('--profile', type=str, required=False)

    if '--wallets' in sys.argv:
        parser.add_argument('--wallets', type=str, required=False)

    if '--private_keys' in sys.argv:
        parser.add_argument('--private_keys', type=str, required=False)

    if '--cex_addresses' in sys.argv:
        parser.add_argument('--cex_addresses', type=str, required=False)

    if '--starknet_addresses' in sys.argv:
        parser.add_argument('--starknet_addresses', type=str, required=False)

    if '--account_csv' in sys.argv:
        parser.add_argument('--account_csv', type=str, required=False)

    if '--proxy_file' in sys.argv:
        parser.add_argument('--proxy_file', type=str, required=False)

    if '--password' in sys.argv:
        parser.add_argument('--password', type=str, required=False)

    if '--network' in sys.argv:
        parser.add_argument('--network', type=str, required=False)

    if '--module' in sys.argv:
        parser.add_argument('--module', type=str, required=False)

    if '--cex_conf' in sys.argv:
        parser.add_argument('--cex_conf', type=str, required=False)

    if '--spreadsheet_id' in sys.argv:
        parser.add_argument('--spreadsheet_id', type=str, required=False)

    args = parser.parse_args()

    return vars(args)


def parse_profile():
    parser = argparse.ArgumentParser(description='Process arguments.')

    parser.add_argument('--profile', type=str, required=False,
                        default=os.environ.get('PROFILE', 'default'),
                        help='a string to be processed')

    args, unknown = parser.parse_known_args()
    return args.profile
