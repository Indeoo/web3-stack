import requests


def debank_request(address):
    url = "https://pro-openapi.debank.com/v1/user/total_balance"
    params = {
        'id': address
    }
    headers = {
        'accept': 'application/json',
        'AccessKey': 'b7b237e1902d1bc66e8fbd1695a0470aac692123'
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data


def debank_total_balance(address):
    return debank_request(address).get('total_usd_value', 0)