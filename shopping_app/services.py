import re
from .scraper import momo, pchome

def concat_products(keyword, site, page=1):
    products = []
    valid_sites = ['momo', 'pchome']
    selected_sites = [s for s in site if s in valid_sites]
    if not selected_sites:
        raise ValueError("Invalid site. Choose either 'momo' or 'pchome'.")
    
    if "momo" in selected_sites:
        products += search_momo(keyword, page)
    if "pchome" in selected_sites:
        products += search_pchome(keyword, page)
    products = sorted(products, key=lambda x: x['price'])
    start = (page - 1) * 9
    end = page * 9
    page_data = products[start:end]

    return page_data


def parse_price(p):
    if isinstance(p, (int, float)):
        return p
    if not isinstance(p, str):
        return float("inf")

    cleaned = re.sub(r"[^\d.]", "", p)
    try:
        return float(cleaned)
    except ValueError:
        return float("inf")


def search_momo(keyword, page=1):
    if not keyword:
        return []

    products = []
    data = momo.scrape_momo(keyword, page)

    if not data:
        return []

    for item in data:
        products.append({
            "name": item['name'],
            "price": parse_price(item['offers']['price']),
            "priceCurrency": item['offers']['priceCurrency'],
            "type": item['offers']['@type'],
            "description": item['description'],
            "image": item['image'],
            "url": item['url'],
            "site": "momo",
        })
    return products

def search_pchome(keyword, page=1):
    if not keyword:
        return []
    products = []
    data = pchome.scrape_pchome(keyword, page)
    if not data:
        return []
    for item in data:
        products.append({
            "name": item['name'],
            "price": parse_price(item['offers']['price']),
            "priceCurrency": item['offers']['priceCurrency'],
            "type": item['offers']['@type'],
            "description": item.get('description', ''),
            "image": item['image'],
            "url": item['url'],
            "rating":item["aggregateRating"]["ratingValue"] if "aggregateRating" in item else None,
            "site": "pchome"
        })
    return products