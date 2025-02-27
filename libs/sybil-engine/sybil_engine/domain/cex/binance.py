from binance.error import ClientError
from binance.spot import Spot

from sybil_engine.domain.cex.cex import CEX
from sybil_engine.utils.decryptor import read_cex_data

from sybil_engine.utils.utils import ConfigurationException

networks = {
    'ZKSYNC': 'ZKSYNCERA',
    'BASE': 'BASE',
    'ARBITRUM': 'ARBITRUM',
    'OPTIMISM': 'OPTIMISM',
}


class Binance(CEX):
    def __init__(self, binance_secret, password):
        apiKey, secretKey = read_cex_data(binance_secret, password)
        self.client = Spot(api_key=apiKey, api_secret=secretKey)

    def withdrawal(self, address, chain, amount, token=['ETH']):
        try:
            self.client.withdraw(token, amount, address, network=networks[chain])
        except ClientError as e:
            raise ConfigurationException(e.error_message)

    def transfer_from_sub_account(self, tokens=['ETH']):
        for sub_account in self._get_sub_accounts():
            assets = self._get_sub_account_balance(sub_account)
            self._transfer_sub_accounts(sub_account, assets)

    def _transfer_sub_accounts(self, sub_account, assets):
        for asset in assets:
            self.client.sub_account_universal_transfer(
                'SPOT', 'SPOT', asset['asset'], asset['free'], fromEmail=sub_account
            )

    def _get_sub_account_balance(self, sub_account):
        balances = self.client.sub_account_assets(sub_account)['balances']
        assets = []
        for balance in balances:
            # Only add assets with a positive available balance
            if float(balance['free']) > 0:
                assets.append({
                    'asset': balance['asset'],
                    'free': balance['free']
                })
        return assets

    def get_binance_deposit_addresses(self):
        emails = self._get_sub_accounts()
        deposit_addresses = []
        for email in emails:
            deposit_addresses += self.client.sub_account_deposit_address(email, 'ETH')
        return deposit_addresses

    def _get_sub_accounts(self):
        response = self.client.sign_request(
            'GET',
            '/sapi/v1/sub-account/list',
            None
        )
        return [sub_account['email'] for sub_account in response['subAccounts']]

    def _convert_asset_to_usd(self, asset, amount):
        # For assets pegged to USD, no conversion is necessary.
        if asset in ['USDT', 'BUSD', 'USDC']:
            return amount
        try:
            # Assume that a trading pair exists with USDT (e.g., BTCUSDT)
            price_info = self.client.ticker_price(symbol=f"{asset}USDT")
            price = float(price_info['price'])
            return amount * price
        except Exception as e:
            # If conversion fails (no such pair, etc.), skip this asset
            return 0.0

    def get_asset_valuation(self):
        """
        Retrieves the total balance (main + sub-accounts) converted to USD.
        """
        total_usd = 0.0

        # Get main account balances
        try:
            account_info = self.client.account()
            for balance in account_info.get('balances', []):
                asset = balance['asset']
                free = float(balance.get('free', 0))
                locked = float(balance.get('locked', 0))
                amount = free + locked
                if amount > 0:
                    total_usd += self._convert_asset_to_usd(asset, amount)
        except ClientError as e:
            raise ConfigurationException(e.error_message)

        # Include sub-account balances
        sub_accounts = self._get_sub_accounts()
        for sub in sub_accounts:
            sub_balances = self._get_sub_account_balance(sub)
            for asset_info in sub_balances:
                asset = asset_info['asset']
                amount = float(asset_info['free'])
                if amount > 0:
                    total_usd += self._convert_asset_to_usd(asset, amount)

        return total_usd
