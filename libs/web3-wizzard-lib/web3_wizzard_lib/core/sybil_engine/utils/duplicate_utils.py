from loguru import logger


def check_duplicates(list_of_dicts, key):
    seen = {}
    duplicates = {}

    for index, dictionary in enumerate(list_of_dicts):
        if key in dictionary:
            value = dictionary[key]
            if value in seen:
                if value not in duplicates:
                    duplicates[value] = [seen[value]]
                duplicates[value].append(index)
            else:
                seen[value] = index

    if duplicates:
        for value, indices in duplicates.items():
            logger.error(f"Duplicate {key} found '{value}'")
        raise ValueError(f"Duplicates found for key '{key}': {duplicates}")