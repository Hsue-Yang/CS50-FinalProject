import requests
from bs4 import BeautifulSoup
import json5 as json

def scrape_pchome(keyword, page=1):
    url = f"https://24h.pchome.com.tw/search/?q={keyword}&p={page}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    try:
        response = requests.get(url, headers=headers)
        print(response)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data from PChome: {e}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    scripts = soup.find('script', type='application/ld+json')
    if not scripts:
        print("No product data found on the page.")
        return []
    try:
        data = json.loads(scripts.string)
        products = [item for item in data if item.get('@type') == 'Product']
        if not products:
            print("No product data found on the page.")
            return []
        return products
    except Exception as e:
        print(f"Error parsing JSON data: {e}")
        return []