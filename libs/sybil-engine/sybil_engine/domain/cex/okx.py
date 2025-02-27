import ccxt
from loguru import logger
from okx import Funding, SubAccount
from okx.Account import AccountAPI
from okx.Funding import FundingAPI
from okx.MarketData import MarketAPI

from sybil_engine.domain.cex.cex import CEX
from sybil_engine.utils.utils import randomized_sleeping

from sybil_engine.utils.decryptor import read_cex_data

networks = {
    'ETH_MAINNET': 'ERC20',
    'ZKSYNC': 'zkSync Era',
    'LINEA': 'Linea',
    'ARBITRUM': 'Arbitrum One',
    'BASE': 'Base',
    'POLYGON': 'Polygon',
    'POLYGON_BRIDGED': 'Polygon (Bridged)',
    'COREDAO': 'CORE',
    'OPTIMISM': 'Optimism',
    'X_LAYER': 'X Layer'
}


def log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None or result['code'] != '0':
            logger.error(f"Error code: {result['code']} Message: {result['msg']}")
        return result

    return wrapper


class OKX(CEX):
    def __init__(self, cex_data, password):
        self.api_key, self.secret_key, self.passphrase = read_cex_data(cex_data, password)
        self.flag = "0"

    @log
    def withdrawal(self, addr, chain, withdraw_amount, token='ETH'):
        if chain == 'POLYGON' and token == 'USDC':
            network = networks["POLYGON_BRIDGED"]
        else:
            network = networks[chain]

        withdraw_network = token + '-' + network

        fundingAPI = Funding.FundingAPI(self.api_key, self.secret_key, self.passphrase, False, self.flag, debug=False)

        fee = self._get_withdrawal_fee(token, withdraw_network)
        balance = float(self.get_okx_balance(token)[0]['availBal'])

        if withdraw_amount == balance:
            withdraw_amount = withdraw_amount - fee

        if withdraw_amount > 0:
            return fundingAPI.withdrawal(ccy=token, amt=withdraw_amount, dest=4, toAddr=addr, fee=fee,
                                         chain=withdraw_network)
        else:
            return None

    def _get_withdrawal_fee(self, symbol_withdraw, chain_name):
        exchange = ccxt.okx({
            'apiKey': self.api_key,
            'secret': self.secret_key,
            'password': self.passphrase,
            'enableRateLimit': True
        })

        currencies = exchange.fetch_currencies()
        for currency in currencies:
            if currency == symbol_withdraw:
                currency_info = currencies[currency]
                network_info = currency_info.get('networks', None)
                if network_info:
                    for network in network_info:
                        network_data = network_info[network]
                        network_id = network_data['id']
                        if network_id == chain_name:
                            withdrawal_fee = currency_info['networks'][network]['fee']
                            if withdrawal_fee == 0:
                                return 0
                            else:
                                return withdrawal_fee

        raise ValueError(f"     не могу получить сумму комиссии, проверьте значения symbolWithdraw и network")

    def transfer_from_sub_account(self, tokens=['ETH']):
        for acc in self._get_sub_accounts()['data']:
            for token in tokens:
                self._transfer_token_from_sub_account(acc['subAcct'], token)

    def _get_sub_accounts(self):
        subAccountAPI = SubAccount.SubAccountAPI(self.api_key, self.secret_key, self.passphrase, False, self.flag,
                                                 debug=False)

        # Get subaccount list
        return subAccountAPI.get_subaccount_list()

    def _transfer_token_from_sub_account(self, acc_name, token):
        amount = self._get_sub_account_balance(acc_name, token)
        if amount > 0:
            logger.info(f"Transfer {amount} {token} from {acc_name} to Main account")
            self._transfer_from_sub_acc(acc_name, amount, token)
            randomized_sleeping({'from': 1, 'to': 1})

    def _get_sub_account_balance(self, acc_name, token):
        subAccountAPI = SubAccount.SubAccountAPI(self.api_key, self.secret_key, self.passphrase, False, self.flag,
                                                 debug=False)

        return float(subAccountAPI.get_funding_balance(acc_name, token)['data'][0]['bal'])

    def _transfer_from_sub_acc(self, acc_name, amount, token):
        subAccountAPI = Funding.FundingAPI(self.api_key, self.secret_key, self.passphrase, False, self.flag,
                                           debug=False)

        return subAccountAPI.funds_transfer(token, amount, 6, 6, type='2', subAcct=acc_name)

    def get_okx_deposit_addresses(self):
        fundingAPI = Funding.FundingAPI(self.api_key, self.secret_key, self.passphrase, False, self.flag, debug=False)
        sub_accounts = fundingAPI.get_deposit_address('ETH')['data']

        return [sub_account['addr'] for sub_account in sub_accounts]

    def get_okx_deposit_address_for_chain(self, chain):
        fundingAPI = Funding.FundingAPI(self.api_key, self.secret_key, self.passphrase, False, self.flag, debug=False)
        depositAddress = fundingAPI.get_deposit_address('ETH')['data']

        return [addr for addr in depositAddress if addr['chain'] == f'ETH-{networks[chain]}']

    def get_okx_balance(self, currencies):
        fundingAPI = Funding.FundingAPI(self.api_key, self.secret_key, self.passphrase, False, self.flag, debug=False)

        return fundingAPI.get_balances(currencies)['data']

    def get_asset_valuation(self, ccy = 'USD'):
        try:
            # Initialize the Funding API client
            funding_client = FundingAPI(
                self.api_key,
                self.secret_key,
                self.passphrase,
                False,  # usually a boolean flag for some extra options
                self.flag,  # "0" for live, "1" for demo
                debug=False
            )
            # Call the asset valuation endpoint
            result = funding_client.get_asset_valuation(ccy=ccy)
            if result.get('code') != '0':
                print("Error fetching asset valuation:", result.get('msg'))
                return None
            # The response data typically contains a field like 'totalAsset' that represents your overall balance.
            return float(result['data'][0]['totalBal'])
        except Exception as e:
            print("Unexpected error:", e)
            return None

