from .base import BaseShoppingParser
import requests

class MomoParser(BaseShoppingParser):
    def fetch_results(self, keyword):
        url = f"https://api.momoshop.com.tw/api/v1/search?q={keyword}"
        res = requests.get(url).json()

        results = []
        for p in res.get("prods", []):
            if keyword.lower() in p.get("name", "").lower():
                results.append({
                    "name": p["name"],
                    "price": p["price"],
                    "link": f"https://www.momoshop.com.tw/goods.momo?i_code={p['Id']}",
                    "source": "momo"
                })
        return results
