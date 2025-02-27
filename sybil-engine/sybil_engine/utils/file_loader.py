import json

from loguru import logger
import os
import inspect

def load_file_rows(path):
    with open(path, "r") as f:
        logger.info(f"Reading {path}")
        return [row.strip() for row in f]


def load_abi(path):
    try:
        # Get the absolute file path of the function that calls `load_abi`.
        caller_path = inspect.stack()[1].filename
        # Get the directory of the caller function
        caller_dir = os.path.dirname(caller_path)
        # Go up in directory structure until you find setup.py or reach the root
        while caller_dir != os.path.dirname(caller_dir):
            if os.path.exists(os.path.join(caller_dir, 'resources')):
                break
            caller_dir = os.path.dirname(caller_dir)
        # Combine the caller's directory with the provided relative path.
        absolute_path = os.path.join(caller_dir, path)
        with open(absolute_path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"No file found at {path}")
        return None




def load_json_resource(path):
    with open(f"resources/{path}", "r") as file:
        return json.load(file)
