def read_private_keys(filename):
    with open(filename, 'r') as file:
        private_keys = file.readlines()
    return [key.strip() for key in private_keys]


def write_data_to_file(filename, encrypted_data):
    with open(filename, 'w') as file:
        for encrypted_key in encrypted_data:
            file.write(encrypted_key.decode() + '\n')


def write_binance_api_to_file(filename, encrypted_data):
    with open(filename, 'w') as file:
        file.write(encrypted_data.decode() + '\n')
