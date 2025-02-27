from cryptography.fernet import Fernet

from pk_encryptor.utils.key_generator import generate_key


def encrypt_private_key(private_key, password):
    key = generate_key(password)
    fernet = Fernet(key)
    return fernet.encrypt(private_key.encode())


def encrypt_private_keys(private_keys, password):
    return [encrypt_private_key(private_key, password) for private_key in private_keys]


def decrypt_private_key(encrypted_private_key, password):
    key = generate_key(password)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_private_key)


def decrypt_data(private_keys, password):
    return [decrypt_private_key(private_key, password) for private_key in private_keys]
