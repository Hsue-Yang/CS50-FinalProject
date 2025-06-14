from .scraper import momo, pchome

def concat_products(keyword, site):
    products = []
    valid_sites = ['momo', 'pchome']
    selected_sites = [s for s in site if s in valid_sites]
    if not selected_sites:
        raise ValueError("Invalid site. Choose either 'momo' or 'pchome'.")
    
    if "momo" in selected_sites:
        products += search_momo(keyword)
    if "pchome" in selected_sites:
        products += search_pchome(keyword)
    if not products:
        return []
    
    return products

def search_momo(keyword):
    if not keyword:
        return []

    products = []
    data = momo.scrape_momo(keyword)

    if not data:
        return []

    for item in data:
        products.append({
            "name": item['name'],
            "price": item['offers']['price'],
            "priceCurrency": item['offers']['priceCurrency'],
            "type": item['offers']['@type'],
            "description": item['description'],
            "image": item['image'],
            "url": item['url'],
            "site": "momo",
        })
    return products

def search_pchome(keyword):
    if not keyword:
        return []
    products = []
    data = pchome.scrape_pchome(keyword)
    if not data:
        return []
    for item in data:
        products.append({
            "name": item['name'],
            "price": item['offers']['price'],
            "priceCurrency": item['offers']['priceCurrency'],
            "type": item['offers']['@type'],
            "description": item.get('description', ''),
            "image": item['image'],
            "url": item['url'],
            "rating":item["aggregateRating"]["ratingValue"] if "aggregateRating" in item else None,
            "site": "pchome"
        })
    return products