from sybil_engine.contract.contract import Contract
from sybil_engine.contract.transaction_executor import evm_transaction
from sybil_engine.data.tokens import get_tokens_for_chain

from sybil_engine.utils.file_loader import load_abi
from web3 import Web3

abi = load_abi("resources/abi/velocore_pool.json")


def to_bytes32(address):
    return Web3.to_bytes(hexstr=address).rjust(32, b'\0')


class VelocorePoolContract(Contract):
    ZERO = '0x0000000000000000000000000000000000000000000000000000000000000000'

    def __init__(self, contract_address, web3):
        self.LVC = get_tokens_for_chain('LINEA')['LVC']
        self.VLP = get_tokens_for_chain('LINEA')['VLP']
        super().__init__(contract_address, web3, abi)

    @evm_transaction
    def deposit(self, account, amount, deposit_token, pool):
        sender = account.address

        txn_params = self.build_generic_data(sender, set_contract_address=False)

        amount_hex = '0x' + format(amount, '064x')
        min_uint_256_hex = '00000000000000000000000000000000'
        inverted_amount = self.invert_int(amount)
        inverted_amount_hex = '0x' + min_uint_256_hex + inverted_amount

        if deposit_token == 'ETH':
            tokenRef = [
                to_bytes32(self.VLP),
                to_bytes32(self.LVC),
                to_bytes32('0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            ]
            deposit = [0, 0, 0]

            txn_params['value'] = amount

            ops = [
                (
                    to_bytes32(f'0x040000000000000000000000{sender[2:]}'),
                    [to_bytes32('0x02000000000000000000000000000000' + format(amount, '032x'))],
                    to_bytes32(self.ZERO)
                ),
                (
                    to_bytes32(f'0x040000000000000000000000{sender[2:]}'),
                    [to_bytes32('0x02000000000000000000000000000000' + inverted_amount)],
                    to_bytes32(self.ZERO)
                ),
                (
                    to_bytes32(f'000000000000000000000000{pool[2:]}'),
                    [
                        to_bytes32('000100000000000000000000000000007fffffffffffffffffffffffffffffff'),
                        to_bytes32('020200000000000000000000000000007fffffffffffffffffffffffffffffff')
                    ],
                    to_bytes32(self.ZERO)
                ),
                (
                    to_bytes32('0500000000000000000000000000000000000000000000000000000000000000'),
                    [to_bytes32('00010000000000000000000000000000ffffffffffffffffffffffffff785a9c')],
                    to_bytes32(self.ZERO)
                ),
                (
                    to_bytes32(f'010000000000000000000000{pool[2:]}'),
                    [
                        to_bytes32('000200000000000000000000000000007fffffffffffffffffffffffffffffff'),
                        to_bytes32('0101000000000000000000000000000000000000000000000000000000000000')
                    ],
                    to_bytes32(self.ZERO)
                )
            ]
        else:
            wstETH = get_tokens_for_chain('LINEA')[deposit_token]
            tokenRef = [
                to_bytes32(wstETH),
                to_bytes32(self.LVC),
                to_bytes32(self.VLP),
                to_bytes32('0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            ]
            deposit = [amount, 0, 0, 0]

            wstETHLP = '0x1D12E25e5516e5aD32F97fE9Edc332Bf4683f487'

            ops = [
                (
                    to_bytes32(f'0x040000000000000000000000{sender[2:]}'),
                    [to_bytes32(amount_hex)],
                    to_bytes32(self.ZERO)
                ),
                (
                    to_bytes32(f'0x040000000000000000000000{sender[2:]}'),
                    [to_bytes32(inverted_amount_hex)],
                    to_bytes32(self.ZERO)
                ),
                (
                    to_bytes32(f'000000000000000000000000{wstETHLP[2:]}'),
                    [
                        to_bytes32('000200000000000000000000000000007fffffffffffffffffffffffffffffff'),
                        to_bytes32('030100000000000000000000000000007fffffffffffffffffffffffffffffff')
                    ],
                    to_bytes32(self.ZERO)
                ),
                (
                    to_bytes32(f'000000000000000000000000{pool[2:]}'),
                    [
                        to_bytes32('020100000000000000000000000000007fffffffffffffffffffffffffffffff'),
                        to_bytes32('030200000000000000000000000000007fffffffffffffffffffffffffffffff')
                    ],
                    to_bytes32(self.ZERO)
                ),
                (
                    to_bytes32('0500000000000000000000000000000000000000000000000000000000000000'),
                    [to_bytes32('02010000000000000000000000000000ffffffffffffffffffffffb4ad12f9cd')],
                    to_bytes32(self.ZERO)
                ),
                (
                    to_bytes32(f'010000000000000000000000{pool[2:]}'),
                    [
                        to_bytes32('0101000000000000000000000000000000000000000000000000000000000000'),
                        to_bytes32('020200000000000000000000000000007fffffffffffffffffffffffffffffff')
                    ],
                    to_bytes32(self.ZERO)
                )
            ]

        contract_txn = self.contract.functions.execute(tokenRef, deposit, ops).build_transaction(txn_params)

        if self.web3.eth.chain_id == 59144:
            contract_txn['gas'] = contract_txn['gas'] * 2

        return contract_txn

    @evm_transaction
    def withdraw(self, account, eth_amount, eth_vlp, pool):
        sender = account.address

        txn_params = self.build_generic_data(sender, set_contract_address=False)

        tokenRef = [
            to_bytes32(self.LVC),
            to_bytes32(self.VLP),
            to_bytes32('0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        ]
        deposit = [0, 0, 0]

        inverted_eth_amount = self.invert_int(eth_amount)
        inverted_eth_vlp = self.invert_int(eth_vlp[0])

        ops = [
            (
                to_bytes32(f'010000000000000000000000{pool[2:]}'),
                [
                    to_bytes32('0001000000000000000000000000000000000000000000000000000000000000'),
                    to_bytes32(f'01000000000000000000000000000000{inverted_eth_vlp}')
                ],
                to_bytes32('0x0000000000000000000000000000000000000000000000000000000000000000')
            ),
            (
                to_bytes32(f'000000000000000000000000{pool[2:]}'),
                [
                    to_bytes32('010200000000000000000000000000007fffffffffffffffffffffffffffffff'),
                    to_bytes32('020100000000000000000000000000007fffffffffffffffffffffffffffffff')
                ],
                to_bytes32('0x0000000000000000000000000000000000000000000000000000000000000000')
            ),
            (
                to_bytes32('0500000000000000000000000000000000000000000000000000000000000000'),
                [to_bytes32(f'02010000000000000000000000000000{inverted_eth_amount}')],
                to_bytes32('0x0000000000000000000000000000000000000000000000000000000000000000')
            )
        ]

        contract_txn = self.contract.functions.execute(tokenRef, deposit, ops).build_transaction(txn_params)

        if self.web3.eth.chain_id == 59144:
            contract_txn['gas'] = contract_txn['gas'] * 2

        return contract_txn

    def allPairs(self):
        return self.contract.functions.allPairs(1).call()

    def facets(self):
        return self.contract.functions.facets().call()

    def invert_int(self, amount):
        max_uint_256_hex = 'ffffffffffffffffffffffffffffffff'
        hex_2 = int(max_uint_256_hex, 16) - amount + 1
        hex_string = hex(hex_2)[2:].rjust(32, '0')

        return hex_string
# 5411000000000000
# 5410999999999999
