from django.db import models

class Website(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)
    api_endpoint = models.URLField(default='https://google.com/search',help_text="網站搜尋API的端點URL")
    api_key = models.CharField(max_length=255, blank=True, null=True, help_text="API金鑰(如果需要)")
    is_active = models.BooleanField(default=True, help_text="是否啟用此網站的搜尋功能")
    search_delay = models.FloatField(default=1.0, help_text="搜尋間隔秒數，避免過於頻繁請求")
    max_results = models.IntegerField(default=50, help_text="單次搜尋最大結果數量")
    
    # 可選：網站的額外設定
    headers = models.JSONField(default=dict, blank=True, help_text="請求標頭設定")
    search_params = models.JSONField(default=dict, blank=True, help_text="搜尋參數設定")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "購物網站"
        verbose_name_plural = "購物網站"

    def __str__(self):
        return self.name
    
    def is_available(self):
        """檢查網站是否可用"""
        return self.is_active and self.api_endpoint