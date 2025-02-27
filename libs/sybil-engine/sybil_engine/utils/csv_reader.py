import csv

from loguru import logger


def read_csv_rows(csv_file_path):
    # Replace 'file.csv' with the path to your CSV file
    logger.info(f"Loading {csv_file_path}")
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)

        rows = []

        for row in csvreader:
            rows.append(row)

        return rows
