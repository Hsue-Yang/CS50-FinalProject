import requests
from bs4 import BeautifulSoup
import json5 as json

def scrape_momo(keyword, page=1):
    url = f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={keyword}&curPage={page}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data from Momo: {e}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    scripts = soup.find('script', type='application/ld+json')
    if not scripts:
        print("No product data found on the page.")
        return []
    try:
        data = json.loads(scripts.string)["mainEntity"]["itemListElement"]
        if not isinstance(data, list):
            data = [data]

        return data
    except Exception as e:
        print(f"Error parsing JSON data: {e}")
        return []
    