from sqlalchemy import create_engine
import pandas as pd

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

def load_to_spreadsheet(df, file_path):
    try:
        df.to_excel(file_path, index=False, engine='openpyxl')
        print("Data berhasil disimpan ke file Excel")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")