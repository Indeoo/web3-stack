from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_starknet_transaction
from sybil_engine.utils.file_loader import load_abi

abi = load_abi("resources/abi/orbiter_starknet.json")


class OrbiterStarknet(Contract):
    def __init__(self, contract_address, web3):
        super().__init__(contract_address, web3, abi)

    @evm_starknet_transaction
    def bridge(self, account, amount):
        txn_params = self.build_generic_data(account.address, False)

        txn_params['value'] = amount.wei

        if account.starknet_address[:3] == '0x0':
            starknet_wallet = f'030{account.starknet_address[3:]}'
        else:
            starknet_wallet = f'030{account.starknet_address[2:]}'

        starknet_wallet = bytes.fromhex(starknet_wallet)

        contract_txn = self.contract.functions.transfer(
            '0x80C67432656d59144cEFf962E8fAF8926599bCF8',
            starknet_wallet
        ).build_transaction(txn_params)

        return contract_txn
