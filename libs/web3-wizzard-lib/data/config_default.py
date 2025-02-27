encryption = True  # Вкл/выкл шифрования приватных ключей
password = 'test'  # Если encryption = False, то пароль не используется

proxy_mode = 'RANDOM'  # [RANDOM, STRICT]
account_create_mode = 'CSV'  # [CSV, TXT] Режим чтения аккаунтов
shell_mode = 'interactive'  # ['classic', 'interactive']
# classic - задавать модуль в module_config_default
# interactive - задавать модуль в консоли во время запуска
interactive_confirmation = True  # Если True - при запуске уточняется правильная ли конфигурация запускается

statistic_config = {
    "mode": "GOOGLE",  # CSV/GOOGLE
    "spreadsheet_id": "",  # required for GOOGLE
}

# Максимальные цены на газ Gwei для каждой сети
gas_prices = {
    'ETH_MAINNET': 50,
    'ZKSYNC': 0.26,
    'BASE': 0.5,
    'LINEA': 2,
    'ARBITRUM': 2,
    'ARBITRUM_NOVA': 2,
    'AVALANCHE': 26,
    'BSC': 5,
    'FANTOM': 750,
    'OPTIMISM': 0.5,
    'POLYGON': 150,
    'SCROLL': 2,
    'ZKFAIR': 10001,
    'COREDAO': 10,
    'MANTA': 0.3,
    'ZORA': 1,
    'POLYGON_ZK': 3,
    'X_LAYER': 10
}

# CEX configuration
cex_data = {
    'okx': '',
    'binance': ''
}
# CEX Withdraw [ZKSYNC, LINEA, BASE, ARBITRUM]
auto_withdrawal = False
withdraw_interval = {'from': 0.01, 'to': 0.015}
min_auto_withdraw_interval = {'from': 0.1, 'to': 0.2}

# Настройки телеграм.
telegram_enabled = False
telegram_api_key = ''
telegram_api_chat_id = 1
telegram_log_level = 'ERROR'  # ['INFO', 'ERROR', 'DEBUG']
