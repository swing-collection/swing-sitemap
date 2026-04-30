from django.db import models
from .model_sitemap_url import URL


class StandardSitemapURL(URL):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return self.url