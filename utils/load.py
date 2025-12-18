from sqlalchemy import create_engine
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SPREADSHEET_ID = '1oY_cgvRV9uk4OcFitaSX2um8ZjgmpRNDU49QLdVeFrI'
RANGE_NAME = 'Sheet1!A2:G868'

def load_to_postgres(df, db_url):
    try:
        engine = create_engine(db_url)

        with engine.connect() as conn:
            df.to_sql('fashion', conn, if_exists='replace', index=False)
            print("Data berhasil dimuat ke database")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def load_to_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        print("Data berhasil disimpan ke file CSV")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def load_to_spreadsheet(df):
    try:
        service = build('sheets', 'v4', credentials=credential)
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body={'values': df.values.tolist()}
        ).execute()
        print("Data berhasil dimuat ke Google Sheets")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")