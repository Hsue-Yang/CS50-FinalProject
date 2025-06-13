import requests
from bs4 import BeautifulSoup

def scrape_momo(keyword):
    url = f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={keyword}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data from Momo: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.select(".prdListArea .listArea li"):
        name_tag = item.select_one('.prdName')
        price_tag = item.select_one('.price')
        img_tag = item.select_one('img')
        link_tag = item.select_one('a')

        if name_tag and price_tag and img_tag and link_tag:
            name = name_tag.get_text(strip=True)
            price = int(price_tag.get_text(strip=True).replace(",", "").replace("元", ""))
            image = img_tag.get('src')
            url = "https://www.momoshop.com.tw" + link_tag.get('href')

            products.append({
                "name": name,
                "price": price,
                "originalPrice": price,  # momo 很少寫原價，有的話可以抓
                "image": image,
                "site": "momo",
                "siteName": "momo購物",
                "rating": 4.5,  # 假資料，你可以自己擴充
                "reviews": 100,
                "inStock": True,
                "url": url,
            })
    
    return products