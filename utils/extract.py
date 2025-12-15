import requests
import pandas as pd
from bs4 import BeautifulSoup
 
# User Agent
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetch_url(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def extract_products_detail(product):
    product_detail = product.find("div", class_="product-details")
    title = product_detail.find("h3").text
    price_container = product_detail.find("div", class_="price-container")
    if price_container:
        price = price_container.find("span", class_="price").text
    else:
        price = None
    paragraph = product_detail.find_all("p")
    for p in paragraph:
        if "Rating" in p.text:
            rating = p.text
        elif "Colors" in p.text:
            colors = p.text
        elif "Size" in p.text:
            size = p.text
        else:
            gender = p.text
    
    return {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender
    }

def scrape_products(url):
    content = fetch_url(url)
    if not content:
        return []

    soup = BeautifulSoup(content, "html.parser")
    data = []
    collection = soup.find("div", class_="collection-grid", id="collectionList")

    if collection:
        products = collection.find_all("div", class_="collection-card")
        for product in products:
            product_details = extract_products_detail(product)
            data.append(product_details)
    return data
    
def main():
    base_url = "https://fashion-studio.dicoding.dev"
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
        df.to_csv("products.csv", index=False)
        print(df.head())
    else:
        print("Failed to scrape products.")
    
if __name__ == "__main__":
    main()