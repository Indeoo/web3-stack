from web3_wizzard_lib.core.sybil_engine.contract import Contract
from web3_wizzard_lib.core.sybil_engine.data.networks import get_ids_chain
from web3_wizzard_lib.core.sybil_engine.data.tokens import get_tokens_for_chain

abi = 'test'


class MendiFinanceContract(Contract):
    def __init__(self, contract_address, web3):
        self.weth_token = get_tokens_for_chain(get_ids_chain()[web3.eth.chain_id])['WETH']
        super().__init__(contract_address, web3, abi)
