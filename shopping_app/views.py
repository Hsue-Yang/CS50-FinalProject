from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Website
from typing import List, Dict, Any
from django.core.cache import cache
import requests
import time
import logging
logger = logging.getLogger(__name__)
# request -> response
def home(request):
    return render(request, 'home.html', {
        'title': 'Home Page',
        'message': 'Welcome to the Shopping App!'
    })

def index(request):
    fake_websites = [
        {'id': 1, 'name': 'PChome', 'url': 'https://www.pchome.com.tw', 'is_active': True},
        {'id': 2, 'name': 'momo購物網', 'url': 'https://www.momoshop.com.tw', 'is_active': True},
        {'id': 3, 'name': '蝦皮商城', 'url': 'https://shopee.tw', 'is_active': True},
        {'id': 4, 'name': 'Yahoo購物中心', 'url': 'https://tw.buy.yahoo.com', 'is_active': True},
        {'id': 5, 'name': 'ETMall東森購物', 'url': 'https://www.etmall.com.tw', 'is_active': True},
        {'id': 6, 'name': '森森購物網', 'url': 'https://www.u-mall.com.tw', 'is_active': True},
    ]
    
    # 創建假精選商品
    fake_featured_products = [
        {
            'name': 'iPhone 15 Pro Max 256GB',
            'price': 48900,
            'original_price': 52900,
            'image_url': 'https://picsum.photos/300/300?random=101',
            'website': {'name': 'momo購物網'},
            'rating': 4.8,
            'reviews_count': 256,
            'discount_percentage': 7.6,
        },
        {
            'name': 'MacBook Air M3 13吋',
            'price': 39900,
            'original_price': 41900,
            'image_url': 'https://picsum.photos/300/300?random=102',
            'website': {'name': 'PChome'},
            'rating': 4.9,
            'reviews_count': 189,
            'discount_percentage': 4.8,
        },
        {
            'name': 'Sony WH-1000XM5 無線耳機',
            'price': 9990,
            'original_price': 11990,
            'image_url': 'https://picsum.photos/300/300?random=103',
            'website': {'name': '蝦皮商城'},
            'rating': 4.7,
            'reviews_count': 445,
            'discount_percentage': 16.7,
        },
        {
            'name': 'LG 27吋 4K顯示器',
            'price': 12900,
            'original_price': 15900,
            'image_url': 'https://picsum.photos/300/300?random=104',
            'website': {'name': 'Yahoo購物中心'},
            'rating': 4.6,
            'reviews_count': 78,
            'discount_percentage': 18.9,
        },
    ]
    
    # 創建假熱門搜尋
    fake_popular_searches = [
        {'keyword': 'iPhone'},
        {'keyword': '筆記型電腦'},
        {'keyword': '無線耳機'},
        {'keyword': '機械鍵盤'},
        {'keyword': '電競滑鼠'},
    ]
    
    context = {
        'websites': fake_websites,
        'featured_products': fake_featured_products,
        'popular_searches': fake_popular_searches,
    }
    return render(request, 'index.html', context)

def search(request):
    # 取得所有啟用的網站資料供篩選使用
    websites = Website.objects.filter(is_active=True)
    
    # 初始化搜尋參數
    query = request.GET.get('q', '').strip()
    selected_websites = request.GET.getlist('websites')
    sort_by = request.GET.get('sort', 'price')
    page = int(request.GET.get('page', 1))
    
    context = {
        'query': query,
        'websites': websites,
        'selected_websites': [int(w) for w in selected_websites if w.isdigit()],
        'sort_by': sort_by,
        'products': [],
        'total_results': 0,
        'error_message': None,
    }
    
    # 只有在有查詢關鍵字時才進行搜尋
    if query:
        try:
            # 決定要搜尋的網站
            if selected_websites:
                search_websites = websites.filter(id__in=selected_websites)
            else:
                search_websites = websites
            
            # 使用搜尋服務進行實際搜尋
            search_service = ProductSearchService()
            all_products = search_service.search_products(
                query=query,
                websites=search_websites,
                sort_by=sort_by
            )
            
            # 分頁處理，每頁顯示 12 筆
            paginator = Paginator(all_products, 12)
            paginated_products = paginator.get_page(page)
            
            context.update({
                'products': paginated_products,
                'total_results': len(all_products),
            })
            
        except Exception as e:
            logger.error(f"搜尋過程中發生錯誤: {str(e)}")
            context['error_message'] = "搜尋過程中發生錯誤，請稍後再試。"
    
    return render(request, 'search.html', context)

class ProductSearchService:
    """商品搜尋服務類"""
    
    def __init__(self):
        self.session = requests.Session()
        # 設定通用的請求標頭
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_products(self, query: str, websites: List[Website], sort_by: str = 'price') -> List[Dict[str, Any]]:
        """
        從多個網站搜尋商品
        
        Args:
            query: 搜尋關鍵字
            websites: 要搜尋的網站列表
            sort_by: 排序方式
            
        Returns:
            商品列表
        """
        all_products = []
        
        for website in websites:
            try:
                # 檢查快取
                cache_key = f"search_{website.id}_{query}"
                cached_results = cache.get(cache_key)
                
                if cached_results:
                    all_products.extend(cached_results)
                    logger.info(f"從快取獲取 {website.name} 的搜尋結果")
                else:
                    # 實際搜尋
                    products = self._search_website(website, query)
                    if products:
                        all_products.extend(products)
                        # 快取結果 10 分鐘
                        cache.set(cache_key, products, 600)
                        logger.info(f"從 {website.name} 獲取到 {len(products)} 個商品")
                
                # 避免過於頻繁的請求
                time.sleep(website.search_delay)
                
            except Exception as e:
                logger.error(f"搜尋 {website.name} 時發生錯誤: {str(e)}")
                continue
        
        # 排序商品
        all_products = self._sort_products(all_products, sort_by)
        
        return all_products
    
    def _search_website(self, website: Website, query: str) -> List[Dict[str, Any]]:
        """
        搜尋單一網站
        
        Args:
            website: 網站模型
            query: 搜尋關鍵字
            
        Returns:
            商品列表
        """
        # 這裡需要根據不同網站實作不同的搜尋邏輯
        # 目前先返回模擬資料
        return self._generate_mock_products(website, query)
    
    def _generate_mock_products(self, website: Website, query: str, count: int = 10) -> List[Dict[str, Any]]:
        """生成模擬商品資料用於測試"""
        import random
        
        categories = {
            '筆記型電腦': [
                'ASUS VivoBook', 'Acer Aspire', 'HP Pavilion', 'Lenovo IdeaPad', 
                'MSI Modern', 'Dell Inspiron', 'MacBook Air', 'Surface Laptop'
            ],
            '手機': [
                'iPhone 15', 'Samsung Galaxy S24', 'Google Pixel 8', 'OPPO Find X7',
                'Xiaomi 14', 'OnePlus 12', 'Vivo X100', 'Realme GT5'
            ],
            '耳機': [
                'Sony WH-1000XM5', 'Bose QuietComfort', 'AirPods Pro', 'Sennheiser HD',
                'Audio-Technica ATH', 'Beyerdynamic DT', 'JBL Tune', 'Marshall Major'
            ],
            '鍵盤': [
                'Logitech MX Keys', 'Corsair K95', 'Razer BlackWidow', 'SteelSeries Apex',
                'Keychron K8', 'HHKB Professional', 'Ducky One 3', 'Leopold FC'
            ],
            '滑鼠': [
                'Logitech MX Master', 'Razer DeathAdder', 'SteelSeries Rival', 'Corsair Dark Core',
                'ASUS ROG Gladius', 'Zowie EC2', 'Glorious Model O', 'Roccat Kone'
            ],
            '螢幕': [
                'ASUS ProArt', 'LG UltraWide', 'Samsung Odyssey', 'Dell UltraSharp',
                'Acer Predator', 'BenQ PD', 'AOC CU34G2X', 'ViewSonic VX'
            ]
        }
        
        # 根據查詢關鍵字選擇相關產品
        relevant_products = []
        for category, products in categories.items():
            if query.lower() in category.lower():
                relevant_products.extend(products)
        
        # 如果沒有找到相關類別，使用所有產品
        if not relevant_products:
            for products in categories.values():
                relevant_products.extend(products)
        
        mock_products = []
        for i in range(count):
            base_name = random.choice(relevant_products)
            variants = ['標準版', '進階版', '專業版', 'Pro', 'Max', 'Ultra', 'Plus']
            product_name = f"{base_name} {random.choice(variants)}"
            
            # 價格設定
            base_price = random.uniform(500, 50000)
            discount = random.choice([0, 5, 10, 15, 20, 25, 30])
            original_price = base_price if discount > 0 else None
            current_price = base_price * (1 - discount / 100)
            
            mock_product = {
                'name': product_name,
                'price': round(current_price, 2),
                'original_price': round(original_price, 2) if original_price else None,
                'image_url': f'https://picsum.photos/300/300?random={website.id}0{i}',
                'product_url': f'{website.url}/product/{i+1}',
                'website': {
                    'id': website.id,
                    'name': website.name,
                    'url': website.url
                },
                'description': f'高品質的{product_name}，採用最新技術，性能卓越，是您的最佳選擇。',
                'rating': round(random.uniform(3.5, 5.0), 1),
                'reviews_count': random.randint(10, 999),
                'in_stock': random.choice([True, True, True, False]),  # 75%有庫存
                'discount_percentage': discount,
            }
            mock_products.append(mock_product)
        
        return mock_products
    
    def _sort_products(self, products: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
        """
        排序商品列表
        
        Args:
            products: 商品列表
            sort_by: 排序方式
            
        Returns:
            排序後的商品列表
        """
        if sort_by == 'price':
            return sorted(products, key=lambda x: x['price'])
        elif sort_by == 'price_desc':
            return sorted(products, key=lambda x: x['price'], reverse=True)
        elif sort_by == 'rating':
            return sorted(products, key=lambda x: x.get('rating', 0), reverse=True)
        elif sort_by == 'name':
            return sorted(products, key=lambda x: x['name'])
        else:
            return products
    
    def search_specific_website(self, website: Website, query: str) -> List[Dict[str, Any]]:
        """
        搜尋特定網站的商品
        這裡需要根據不同網站實作具體的搜尋邏輯
        """
        # 根據網站名稱或ID判斷使用哪種搜尋方法
        if 'momo' in website.name.lower():
            return self._search_momo(query)
        elif 'pchome' in website.name.lower():
            return self._search_pchome(query)
        elif 'shopee' in website.name.lower() or '蝦皮' in website.name:
            return self._search_shopee(query)
        # 可以繼續添加其他網站的搜尋方法
        else:
            # 預設使用通用搜尋方法
            return self._search_generic(website, query)
    
    def _search_momo(self, query: str) -> List[Dict[str, Any]]:
        """搜尋momo購物網的商品"""
        # 實作momo的搜尋邏輯
        # 這裡需要根據momo的API文件來實作
        pass
    
    def _search_pchome(self, query: str) -> List[Dict[str, Any]]:
        """搜尋PChome的商品"""
        # 實作PChome的搜尋邏輯
        pass
    
    def _search_shopee(self, query: str) -> List[Dict[str, Any]]:
        """搜尋蝦皮商城的商品"""
        # 實作蝦皮的搜尋邏輯
        pass
    
    def _search_generic(self, website: Website, query: str) -> List[Dict[str, Any]]:
        """通用搜尋方法"""
        # 使用網站的API設定進行搜尋
        pass