import json
import os

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import io
import csv

from loguru import logger


def get_google_spreadsheet(spreadsheet_id, sheet_name):
    # Spreadsheet details
    service = build('sheets', 'v4', credentials=get_google_credentials())

    # Call the Sheets API to fetch data
    sheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()

    logger.info(f"Loaded {sheet_name} from {spreadsheet_id}")

    data = sheet.get('values', [])

    csv_file_like = io.StringIO()
    csv_file_like.write('\n'.join([','.join(map(str, row)) for row in data]))
    csv_file_like.seek(0)
    # Now, use csv.DictReader to read this "file"
    reader = csv.DictReader(csv_file_like)

    rows = []
    for row in reader:
        rows.append(row)

    csv_file_like.close()

    return rows


def get_google_credentials():
    return Credentials.from_service_account_info(json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT']))
