import requests
from bs4 import BeautifulSoup
from .scraper import momo
import json
import re
from urllib.parse import quote

def crawl_momo(keyword):
    url = f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={keyword}"
    headers = {-"Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    products=[]
    if res.status_code != 200:
        return []

    for item in soup.select(".prdListArea .listArea li"):
        title_tag = item.select_one(".prdName")
        price_tag = item.select_one(".price")

        if title_tag and price_tag:
            products.append({
                "title": title_tag.text.strip(),
                "price": price_tag.text.strip(),
                "link": "https://www.momoshop.com.tw" + title_tag.get("href")
            })
    return products

if __name__ == "__main__":
    results = crawl_momo("iphone")
    for product in results:
        print(f"Title: {product['title']}, Price: {product['price']}, Link: {product['link']}")

def search_products(keyword):
    if not keyword:
        return []

    results = momo.scrape_momo(keyword)
    
    if not results:
        return []

    products = []
    for item in results:
        products.append({
            "title": item.get("title", ""),
            "price": item.get("price", "")
        })
    
    return products

def search_momo(self, keyword, max_results=10):
        """搜尋 momo 購物網"""
        try:
            url = f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={quote(keyword)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []
            
            # 解析 JSON-LD 結構化數據
            json_scripts = soup.find_all('script', type='application/ld+json')
            
            for script in json_scripts:
                try:
                    data = json.loads(script.string)
                    if (data.get('@type') == 'WebPage' and 
                        'mainEntity' in data and 
                        data['mainEntity'].get('@type') == 'ItemList'):
                        
                        items = data['mainEntity'].get('itemListElement', [])
                        
                        for item in items[:max_results]:
                            if item.get('@type') == 'Product':
                                offers = item.get('offers', {})
                                
                                # 提取折扣資訊
                                description = item.get('description', '')
                                discount_match = re.search(r'折(\d+)', description)
                                discount = int(discount_match.group(1)) if discount_match else 0
                                
                                product = {
                                    'name': item.get('name', ''),
                                    'price': float(offers.get('price', 0)),
                                    'image_url': item.get('image', ''),
                                    'product_url': item.get('url', ''),
                                    'site': 'momo',
                                    'site_name': 'momo購物網',
                                    'discount': discount,
                                    'in_stock': 'InStock' in offers.get('availability', ''),
                                    'currency': 'TWD'
                                }
                                
                                if product['name'] and product['price'] > 0:
                                    products.append(product)
                        break
                except (json.JSONDecodeError, KeyError):
                    continue
            
            return products
            
        except Exception as e:
            print(f"momo 搜尋錯誤: {e}")
            return []