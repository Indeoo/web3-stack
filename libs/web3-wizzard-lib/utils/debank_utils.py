import requests


def debank_request(address):
    url = "https://pro-openapi.debank.com/v1/user/total_balance"
    params = {
        'id': address
    }
    headers = {
        'accept': 'application/json',
        'AccessKey': '6cd56a970242386fa2a57e380c39f00f10b31778'
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data


def debank_total_balance(address):
    return debank_request(address).get('total_usd_value', 0)