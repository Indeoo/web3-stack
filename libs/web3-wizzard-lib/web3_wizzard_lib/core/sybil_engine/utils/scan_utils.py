import requests
from web3 import Web3


def find_interacted_contracts(wallet_address, api_url, api_key):
    api_url = f"{api_url}/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=latest&sort=asc&apikey={api_key}"

    response = requests.get(api_url)
    data = response.json()

    contracts = set()  # Use a set to avoid duplicates

    if data['status'] == '1' and data['message'] == 'OK':
        for tx in data['result']:
            if tx['to']:  # Assuming non-empty 'to' indicates potential contract interaction
                contracts.add(Web3.to_checksum_address(tx['to']))

    return contracts


def find_interacted_data(wallet_address, api_url, api_key):
    api_url = f"{api_url}/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=latest&sort=asc&apikey={api_key}"

    response = requests.get(api_url)
    data = response.json()

    contracts = set()  # Use a set to avoid duplicates

    if data['status'] == '1' and data['message'] == 'OK':
        for tx in data['result']:
            if tx['to']:  # Assuming non-empty 'to' indicates potential contract interaction
                contracts.add(Web3.to_checksum_address(tx['data']))

    return contracts
