from utils.extract import scrape_products
from utils.transform import transform_data
from utils.transform import cleaned_data
from utils.load import load_to_postgres
from utils.load import load_to_csv
from utils.load import load_to_spreadsheet

base_url = "https://fashion-studio.dicoding.dev"
postgres_url = "postgresql://dev:pw123@localhost:5432/fashion_db"
exchange_rate = 16000
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