from django.db import models

class Website(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)
    api_endpoint = models.URLField(default='https://google.com/search',help_text="網站搜尋API的端點URL")
    is_active = models.BooleanField(default=True, help_text="是否啟用此網站的搜尋功能")
    
    # 可選：網站的額外設定
    headers = models.JSONField(default=dict, blank=True, help_text="請求標頭設定")
    search_params = models.JSONField(default=dict, blank=True, help_text="搜尋參數設定")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def is_available(self):
        """檢查網站是否可用"""
        return self.is_active and self.api_endpoint