import requests
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.domain.dex import Dex
from sybil_engine.utils.gas_utils import l1_gas_price
from sybil_engine.utils.utils import randomized_sleeping, SwapException
from web3 import Web3


class OneInch(Dex):
    dex_name = '1inch'
    swap_contract = '1INCH'
    supported_chains = ['BASE', 'ZKSYNC', 'OPTIMISM', 'ARBITRUM']

    def __init__(self, chain_instance, web3):
        super().__init__(chain_instance, web3)
        self.weth_address = self.tokens['WETH']
        self.base_url = 'https://api.1inch.dev/swap'
        self.inch_version = 5.2

    @l1_gas_price
    def swap(self, amount_to_swap, from_token, to_token, slippage, account):
        if amount_to_swap.wei == 0:
            raise SwapException(f"Can't swap 0 of {amount_to_swap.token}")

        self.get_txn(account, amount_to_swap, from_token, to_token)

    def get_api_call_data(self, url):
        response = requests.get(url, headers={'Authorization': "DuagMR3vHpYc9JBNqM0Wx9mSWA7VzwuH"})

        return response.json()

    @evm_transaction
    def get_txn(self, account, amount_to_swap, from_token, to_token):
        spender_json = self.get_api_call_data(
            f'{self.base_url}/v{self.inch_version}/{self.web3.eth.chain_id}/approve/spender')
        spender = Web3.to_checksum_address(spender_json['address'])

        if from_token.symbol() != 'ETH' and from_token.allowance(account, spender) < amount_to_swap.wei:
            from_token.approve(account, spender)

        randomized_sleeping({'from': 1, 'to': 5})

        _1inchurl = f"{self.base_url}/v{self.inch_version}/{self.web3.eth.chain_id}/swap?fromTokenAddress={from_token.address()}&toTokenAddress={to_token.address()}&amount={amount_to_swap.wei}&fromAddress={account.address}&slippage=5"
        json_data = self.get_api_call_data(_1inchurl)

        if json_data is False:
            raise Exception(json_data['description'])

        contract_txn = json_data['tx']
        contract_txn['from'] = Web3.to_checksum_address(contract_txn['from'])
        contract_txn['chainId'] = self.web3.eth.chain_id
        contract_txn['nonce'] = self.web3.eth.get_transaction_count(account.address)
        contract_txn['to'] = Web3.to_checksum_address(contract_txn['to'])
        contract_txn['gasPrice'] = int(contract_txn['gasPrice'])
        contract_txn['gas'] = int(contract_txn['gas'])
        contract_txn['value'] = int(contract_txn['value'])

        return contract_txn
