def load_addresses(path):
    with open(path, "r") as f:
        from loguru import logger
        logger.info(f"Reading {path}")

        keys = []

        for row in f:
            keys = keys + [row.strip()]

        return keys
