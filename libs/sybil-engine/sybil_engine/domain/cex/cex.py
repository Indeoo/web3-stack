from sybil_engine.config.app_config import get_cex_data

class CEX:
    def withdrawal(self, addr, chain, withdraw_amount, token='ETH'):
        pass

    def transfer_from_sub_account(self, tokens=['ETH']):
        pass

    def get_asset_valuation(self):
        pass


def get_cex_addresses(cex_conf):
    password, cex_data = get_cex_data()

    return None
    #return get_okx_deposit_addresses(password, cex_data[cex_conf]) #+ get_binance_deposit_addresses(password, cex_data['binance'])
