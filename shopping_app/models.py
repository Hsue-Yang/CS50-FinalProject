from django.db import models

class Website(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)
    api_endpoint = models.URLField(default='https://google.com/search',help_text="The endpoint URL of the website's search API")
    is_active = models.BooleanField(default=True, help_text="Whether the search function for this website is enabled")
    
    headers = models.JSONField(default=dict, blank=True, help_text="Request header configuration")
    search_params = models.JSONField(default=dict, blank=True, help_text="Search parameter configuration")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def is_available(self):
        return self.is_active and self.api_endpoint