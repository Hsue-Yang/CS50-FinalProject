from .base import BaseShoppingParser
import requests

class ShopeeParser(BaseShoppingParser):
    def fetch_results(self, keyword):
        url = f"https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword={keyword}&limit=10&newest=0&order=desc&page_type=search"
        res = requests.get(url).json()

        results = []
        for item in res.get("items", []):
            item_basic = item.get("item_basic", {})
            if keyword.lower() in item_basic.get("name", "").lower():
                results.append({
                    "name": item_basic["name"],
                    "price": item_basic["price"] // 100000,  # Shopee price 是 int 分為單位
                    "link": f"https://shopee.tw/product/{item['shopid']}/{item['itemid']}",
                    "source": "shopee"
                })
        return results
