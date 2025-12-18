import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

from utils.extract import scrape_products
from utils.transform import transform_data
from utils.transform import cleaned_data
from utils.load import load_to_postgres
from utils.load import load_to_csv
from utils.load import load_to_spreadsheet

base_url = os.getenv("BASE_URL")
postgres_url = os.getenv("POSTGRES_URL")
exchange_rate = int(os.getenv("EXCHANGE_RATE"))
all_data = []

for page in range(1, 51):
    print(f"Scraping page {page}...")
    if page == 1:
        url = base_url
    else:
        url = f"{base_url}/page{page}"
    
    data = scrape_products(url)
    if data:
        all_data.extend(data)

if all_data:
    df = pd.DataFrame(all_data) 
    df = transform_data(df, exchange_rate=exchange_rate)
    df = cleaned_data(df)
    load_to_postgres(df, db_url=postgres_url)
    load_to_csv(df, file_path="products.csv")
    load_to_spreadsheet(df)
    print(df.head())
else:
    print("Failed to scrape products.")