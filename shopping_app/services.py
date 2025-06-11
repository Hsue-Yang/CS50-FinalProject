# management/commands/add_default_websites.py
# 檔案路徑: your_app/management/commands/add_default_websites.py

from django.core.management.base import BaseCommand
from django.db import transaction
from shopping_app.models import Website  # 請根據您的app名稱調整

class Command(BaseCommand):
    help = '新增預設的購物網站資料'

    def handle(self, *args, **options):
        default_websites = [
            {
                'name': 'PChome',
                'url': 'https://www.pchome.com.tw',
                'api_endpoint': 'https://24h.pchome.com.tw/search',
                'is_active': True,
                'search_delay': 1.0,
                'max_results': 50,
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                },
                'search_params': {
                    'q': '',  # 搜尋關鍵字參數名稱
                    'page': 1,
                    'size': 20,
                }
            },
            {
                'name': 'momo購物網',
                'url': 'https://www.momoshop.com.tw',
                'api_endpoint': 'https://m.momoshop.com.tw/search.momo',
                'is_active': True,
                'search_delay': 1.2,
                'max_results': 50,
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                },
                'search_params': {
                    'keyword': '',  # momo使用keyword參數
                    'page': 1,
                    'size': 20,
                }
            },
            {
                'name': '蝦皮商城',
                'url': 'https://shopee.tw',
                'api_endpoint': 'https://shopee.tw/api/v4/search/search_items',
                'is_active': True,
                'search_delay': 1.5,
                'max_results': 50,
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                },
                'search_params': {
                    'keyword': '',
                    'limit': 20,
                    'offset': 0,
                }
            },
            {
                'name': 'Yahoo購物中心',
                'url': 'https://tw.buy.yahoo.com',
                'api_endpoint': 'https://tw.buy.yahoo.com/search/product',
                'is_active': True,
                'search_delay': 1.0,
                'max_results': 50,
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                },
                'search_params': {
                    'p': '',  # Yahoo使用p參數
                    'page': 1,
                }
            },
            {
                'name': 'ETMall東森購物',
                'url': 'https://www.etmall.com.tw',
                'api_endpoint': 'https://www.etmall.com.tw/api/search',
                'is_active': True,
                'search_delay': 1.0,
                'max_results': 50,
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                },
                'search_params': {
                    'keyword': '',
                    'page': 1,
                }
            },
            {
                'name': '森森購物網',
                'url': 'https://www.u-mall.com.tw',
                'api_endpoint': 'https://www.u-mall.com.tw/api/search',
                'is_active': True,
                'search_delay': 1.0,
                'max_results': 50,
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                },
                'search_params': {
                    'q': '',
                    'page': 1,
                }
            },
        ]

        with transaction.atomic():
            for website_data in default_websites:
                website, created = Website.objects.get_or_create(
                    name=website_data['name'],
                    defaults=website_data
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'成功新增網站: {website.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'網站已存在: {website.name}')
                    )

        self.stdout.write(
            self.style.SUCCESS('預設網站資料設定完成！')
        )