import requests
from loguru import logger
from sybil_engine.config.app_config import get_cex_conf, get_cex_data
from sybil_engine.domain.balance.balance import NativeBalance, Erc20Balance
from sybil_engine.domain.balance.balance_utils import get_native_balance
from sybil_engine.domain.balance.tokens import Erc20Token
from sybil_engine.domain.cex.okx import OKX

total_zro = 0

def claimer_zro(account, chain_instance, token, web3):
    allocation_data = get_allocation(account.address)
    if not allocation_data:
        raise Exception("Failed to fetch allocation data.")
    amount_raw = int(allocation_data.get('zroAllocation', {}).get('asBigInt'))
    logger.info(f"ZRO Allocation for {account.address} is {amount_raw}")
    if token == 'NATIVE':
        withdraw_token = chain_instance['gas_token']
        claim_price = NativeBalance(int((round(amount_raw / 10 ** 18) + 1) * 0.00005 * 10 ** 18),
                                    chain_instance['chain'], token)
        balance = get_native_balance(account, web3, chain_instance)
        logger.info(f"Native balance is {balance}")
    else:
        claim_price = Erc20Balance(
            int((round(amount_raw / 10 ** 18) + 1) * 0.00003 * 10 ** 18),
            chain_instance['chain'],
            token,
            decimal=18
        )
        withdraw_token = token
        balance = Erc20Token(chain_instance['chain'], token, web3).balance(account)
        logger.info(f"Native balance is {balance}")
    logger.info(f"Need {claim_price} for claim")
    if claim_price.wei > balance.wei:
        password, cex_data = get_cex_data()
        cex_obj = OKX(cex_data[get_cex_conf()], password)
        cex_obj.withdrawal(account.address, chain_instance['chain'], float(balance.readable()), withdraw_token)

    proof = get_proof(account.address)
    logger.info(proof)
    global total_zro
    total_zro = total_zro + int(proof['amount'])
    amount_to_claim = int(proof['amount'])
    merkle_proof = proof['proof'].split('|')
    #contract_address = get_contracts_for_chain(chain_instance['chain'])['ZRO_CLAIMER']
    #claimer = L0Claim(contract_address, web3)
    #claimer.donateAndClaim(account, claim_price.wei, amount_to_claim, merkle_proof)

def get_proof(wallet):
    url = f"https://www.layerzero.foundation/api/proof/{wallet}?address={wallet}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_allocation(wallet):
    url = f"https://www.layerzero.foundation/api/allocation/{wallet}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None