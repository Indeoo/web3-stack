from datetime import datetime, timedelta

from eth_account.messages import encode_defunct

from sybil_engine.contract.send import Send
from sybil_engine.domain.balance.balance import NativeBalance

from web3_wizzard_lib.core.modules.nft.nft_submodule import NftSubmodule


class LineaWheel(NftSubmodule):
    module_name = 'LINEA_WHEEL'
    nft_address = '0xDb3a3929269281F157A58D91289185F21E30A1e0'

    def execute(self, account, chain='LINEA'):
        data = encode_data(account)

        Send(
            None,
            self.create_web3(account, chain)
        ).send_to_wallet(
            account,
            self.nft_address,
            NativeBalance(0, chain, "ETH"),
            data
        )

    def log(self):
        return "LINEA WHEEL"


def encode_data(account):
    # Function selector
    method_id = "7d5168d1"

    message = "Welcome to Linea Hub. Signing is the only way we can truly know that you are the owner of the wallet you are connecting. Signing is a safe, gas-less transaction that does not in any way give Linea Hub permission to perform any transactions with your wallet."

    r,s,v = sign_message_rsv(message, account)

    # Each parameter is 32 bytes (64 hex chars) - your provided values
    params = [
        "0000000000000000000000000000000000000000000000000000000000000001",  # nonce
        get_timestamp_plus_3h_hex()['hex_timestamp'],  # expirationTimestamp
        "0000000000000000000000000000000000000000000000000000000005f5e100",  # boost
        r,  # signature.r
        s,  # signature.s
        v  # signature.v
    ]

    # Combine all parts
    encoded_data = "0x" + method_id + "".join(params)

    return encoded_data


def get_timestamp_plus_3h_hex():
    """
    Get current timestamp + 3 hours and convert to 32-byte hex format for EVM
    """
    # Get current timestamp
    current_time = datetime.now()

    # Add 3 hours
    future_time = current_time + timedelta(hours=3)

    # Convert to Unix timestamp (seconds since epoch)
    timestamp = int(future_time.timestamp())

    # Convert to hex and pad to 32 bytes (64 hex characters)
    hex_timestamp = format(timestamp, '064x')

    return {
        'current_time': current_time,
        'future_time': future_time,
        'timestamp': timestamp,
        'hex_timestamp': hex_timestamp,
        'hex_with_prefix': f'0x{hex_timestamp}'
    }


def hex_to_readable_time(hex_string):
    """
    Convert hex timestamp back to readable format
    """
    # Remove '0x' prefix if present
    if hex_string.startswith('0x'):
        hex_string = hex_string[2:]

    # Convert hex to integer
    timestamp = int(hex_string, 16)

    # Convert to datetime
    readable_time = datetime.fromtimestamp(timestamp)

    return {
        'timestamp': timestamp,
        'readable_time': readable_time,
        'iso_format': readable_time.isoformat()
    }


def sign_message_rsv(message, account):
    """
    Sign a message and return r, s, v values

    Args:
        message (str): The message to sign
        private_key (str): Private key as hex string (with or without 0x prefix)

    Returns:
        dict: Dictionary containing r, s, v values
    """
    # Create account from private key
    # Encode the message for signing
    encoded_message = encode_defunct(text=message)

    # Sign the message
    signed_message = account.sign_message(encoded_message, account.key)

    # Extract r, s, v values and format as 32-byte hex strings (64 chars)
    r = format(signed_message.r, '064x')
    s = format(signed_message.s, '064x')
    v = format(signed_message.v, '064x')

    return r, s, v