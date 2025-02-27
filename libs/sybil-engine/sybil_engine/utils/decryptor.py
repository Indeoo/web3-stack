import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from loguru import logger


def generate_key(password):
    salt = b'\x87\x12\xac\xa3\x91\xb9\xfe\xb4\x08\x0c\xac\x19\xc6d\x85'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def decrypt_private_key(encrypted_private_key, password):
    key = generate_key(password)
    fernet = Fernet(key)
    decrypted_private_key = fernet.decrypt(encrypted_private_key)
    return decrypted_private_key.decode()


def read_cex_data(cex_data, password):
    try:
        return Fernet(generate_key(password)).decrypt(cex_data).decode('utf-8').split(',')
    except Exception as e:
        logger.warning("Can't read encrypted CEX data, trying to read unencrypted")
        return cex_data
