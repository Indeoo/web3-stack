sleep_interval = {'from': 60 * 5 * 1, 'to': 60 * 10 * 1}  # Sleep interval between accounts
swap_retry_sleep_interval = {'from': 60 * 5 * 1, 'to': 60 * 10 * 1}  # Sleep interval between retries

min_native_interval = {'from': 0.5, 'to': 0.5}

module = "STARGATE_AUTO_BRIDGE" # [Название модуля или сценария]
# Modules: [WARMUP, SELL_ALL, CONCRETE_SWAP, WRAPPING, DMAIL, SEND_TO_CEX, ORBITER,
# BUNGEE, STARGATE_CLASSIC_BRIDGE, STARGATE_AUTO_BRIDGE, STARGATE_FARMING, LENDING, RAGE_WITHDRAW,
# LayerBank, LIQUIDITY_POOL, ZKDX, CEX_SUB_ACCOUNT_TRANSFER, SLEEP_MODULE, MERKLY_REFUEL


# Module [WARMUP, 1]
warmup_config = {
    'auto_withdrawal': False,
    'chain': 'ZKSYNC',
    'swap_amount_interval': '',
    'token': 'ETH',
    'amount_of_warmups': {'from': 3, 'to': 6},
    # 'allowed_dex': ['syncswap','woofi','lineaswap','horizondex''pancake'], #LINEA
    # 'allowed_dex': ['syncswap','mute','woofi','maverick','velocore','pancake','odos'] #ZKSYNC
    # 'allowed dex': ['woofi', 'maverick', 'horizondex', 'pancake', 'odos'] #BASE
    'allowed_dex': ['syncswap', 'mute', 'woofi', 'maverick', 'velocore', 'lineaswap', 'horizondex', 'pancake', 'odos'],
    'warmup_pairs': ['ETH>USDC'],  # specify for warming up by concrete pair
    # 'warmup_pairs': ['ETH>USDC', 'ETH>USDT'],
    'sell_tokens': True,
    'pair_sleep_interval': {'from': 60 * 15, 'to': 60 * 30}  # Interval between different tokens warm up of 1 account
}

# Module [BUNGEE, 11] Bungee [ZKSYNC, ARBITRUM, BSC, BASE, AVALANCHE, POLYGON, OPTIMISM]
bungee_config = {
    'from_chain': 'BASE',
    'to_chain': 'ZKSYNC',
    'refuel_amount_interval': 'max'
    # ['{'from': 0.001, 'to': 0.002}', '', 'max']
}

# Module [STARGATE_AUTO_BRIDGE, 13] Stargate auto bridge
stargate_auto_bridge_config = {
    'bridge_amount_interval': 'all_balance',
    'bridge_token': 'ETH',
    'end_network': '',  # name of network where all tokens will be collected
    'retry_interval': {'from': 60 * 15, 'to': 60 * 30},
    'sleep_interval': {'from': 60 * 30, 'to': 60 * 60},
    'only_end_network_bridge': False,  # if True, then only bridge will be to END NETWORK
    'original_chain_sequence': ['ARBITRUM', 'LINEA', 'BASE']
}

# Module [STARGATE_FARMING, 14] Stargate farming
stargate_farming_config = {
    'chain': 'BASE',  # ['BASE, 'LINEA']
    'bridge_amount_interval': 'all_balance',
    'all_balance_mode': 0,
    # 0 - all_balance игнорирует 'chain' и стекает ETH в чейне с максимально большим балансом
    # 1 - all_balance стекает весь баланс указанного 'chain'
    'operation': {'ADD_TO_POOL', 'DEPOSIT'},
    'token': 'ETH',
    'operation_sleep_interval': {'from': 60 * 2, 'to': 60 * 10}
    # 'operation': {'WITHDRAW', 'REDEEM_FROM_POOL'}
}

# Module [SELL_ALL, 2] This module sells all to ETH or USDC
sell_all_config = {
    'chain': 'ZKSYNC',
    'receive_token': 'ETH',  # [USDC, ETH]
    'sleep_interval': {'from': 60 * 30 * 1, 'to': 60 * 60 * 1}  # Interval between selling different tokens of 1 account
}

# Module [CONCRETE_SWAP, 3] Swap concrete pair in concrete DEX
swap_config = {
    'chain': 'LINEA',
    'app': 'syncswap',
    'from_token': 'ETH',
    'to_token': 'USDT',
    'amount_interval': {'from': 0.001, 'to': 0.001}
}

# Module [WRAPPING, 4] [Wrap/Unwrap WETH]
wrap_config = {
    'chain': 'ZKSYNC',
    'action': 'UNWRAP',  # [WRAP, UNWRAP]
    'amount_interval': 'all_balance'
}

# Module [SEND_TO_CEX, 6] Config
send_to_cex_config = {
    'chain': 'ZKSYNC',
    'amount': {'from': 1, 'to': 1},
    'token': 'NATIVE'  # [NATIVE, USDC]
}

# Module [DMAIL, 5] Config
send_dmail_config = {
    'chain': 'ZKSYNC',  # ['ZKSYNC', 'LINEA', 'SCROLL']
    'email_amount': {'from': 3, 'to': 6}
}

# Module [NFT_MINTER, 15] Все NFT пока работают только для ZKSYNC ["TAVAERA", "ZKS_DOMAIN", "ERA_DOMAIN",
# "EMPTY_NFT", "OMNI_SEA", "MERKLY_MINTER", "L2_TELEGRAPH_MINTER", "KREATOR_LAND", "ABBYSWORLD"]
nft_minter = {
    'nft_amount_interval': {'from': 1, 'to': 1},
    'nft_modules': ["SATOSHI_UNIVERSE"],
    'unique_nft': True # Currently only works for linea
}

# Module [LAYERBANK, 23]
layerbank = {
    'action': 'DEPOSIT',
    'sleep_interval': {'from': 60 * 15, 'to': 60 * 45},
}

# Module [LIQUIDITY_POOL, 24]
liquidity_pool = {
    'action': 'DEPOSIT+WITHDRAW',
    'amount': 'all_balance',
    'token': 'ETH',
    'sleep_interval': {'from': 60 * 2, 'to': 60 * 5},
    'dex': 'velocore',
    'chain': 'LINEA'
}

# Module [ZKDX, 25]
zkdx_config = {
    'amount_interval': 'all_balance',  # USDC amount
    'action': 'DEPOSIT'
}

# Module [CEX_SUB_ACCOUNT_TRANSFER, 26]
cex_account_transfer_config = {

}

# Module [MERKLY_REFUEL, 28] Bungee [ZKSYNC, ARBITRUM, ARBITRUM NOVA, BASE, LINEA, OPTIMISM, SCROLL]
merkly_refuel_config = {
    'start_chain': 'ZKSYNC',  # Если '', первый чейн будет RANDOM
    'end_chain': 'ZKSYNC',  # Если '', то последний чейн будет RANDOM
    'chains': ['ZKSYNC', 'ARBITRUM', 'BASE'],  # Список всех чейнов для которых делать Refuel.
    # Должен вмещать в себя start_chain и end_chain
    'refuel_amount_interval': {'from': 0.00005, 'to': 0.00009},
    'sleeping_interval': {'from': 60 * 5, 'to': 60 * 10}
}

# Module [CEX_WITHDRAW, 29] [ZKSYNC, LINEA, BASE, ARBITRUM, COREDAO, POLYGON, X_LAYER]
cex_withdraw = {
    'chain': 'ZKSYNC',
    'withdraw_interval': {'from': 0.01, 'to': 0.015},
    'min_auto_withdraw_interval': {'from': 0.1, 'to': 0.2},
    'token': 'NATIVE',  # [NATIVE, USDC, USDT]
    'cex': 'okx'
}

# Module [COREDAO_BRIDGE_AUTO, 31
coredao_bridge_auto_config = {
    'from_chain': 'COREDAO',
    'to_chain': 'POLYGON',
    'repeats': {'from': 2, 'to': 4},
    'bridge_amount_interval': 'all_balance',
    'sleep_interval': {'from': 60 * 25, 'to': 60 * 40},  # Интервал from_chain -> to_chain и to_chain -> from_chain
    'token': 'USDT'  # [USDC, USDT]
}

# Module [LAYER2_20, 32]
layer_2_20_config = {
    'chain': 'ZKSYNC',
    'to_chains': ['OPTIMISM', 'BASE', 'LINEA', 'ARBITRUM', 'SCROLL'],
    'repeats': {'from': 2, 'to': 4},
}

# Module [BANKING, 34]
banking_config = {
    'bank': 'MENDI_FINANCE',
    'actions': 'SUPPLY', # ['SUPPLY', 'BORROW', 'REPAY', 'REDEEM']
    'supply_token': 'WETH',
    'borrow_token': 'WETH',
    'sleep_interval': {'from': 1 * 5, 'to': 1 * 10},
    'chain': 'LINEA'
}

# Module [CLAIMER, 35]
claimer_config = {
    'chain': 'ARBITRUM',
    'token': 'NATIVE', # NATIVE or USDT or USDC
    'project': 'RABBY'
}

sleep_module_config = {}

# Module [ADS_IMPORT_PROXY, 36]
ads_import_config = {
    'ads_url': 'http://local.adspower.net:50325/api/v1/user'
}

# Module [BRIDGE, 37]
bridge_module = {
    'bridge': 'ORBITER',
    'bridge_amount_interval': 'all_balance',
    'from_chain': 'POLYGON',
    'to_chain': 'ZKSYNC',
    'token': 'USDT'
}

# Module [SMART_CONTRACT_DEPLOYMENT, 38]
smart_contract_deployment = {
    'chain': 'BASE'
}

erc20_balance = {
    'token_address': '0xd83af4fbD77f3AB65C3B1Dc4B38D7e67AEcf599A',
    'chain': 'LINEA'
}