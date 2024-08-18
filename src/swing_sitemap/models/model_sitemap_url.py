# swing_sitemap/models.py
from django.db import models

class SitemapURL(models.Model):
    url = models.URLField()
    priority = models.FloatField(default=0.5)
    changefreq = models.CharField(max_length=10, choices=[
        ('always', 'Always'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('never', 'Never')
    ])
    lastmod = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.url

from django.db import models




class URL(models.Model):
    url = models.URLField()
    priority = models.FloatField(default=0.5)
    changefreq = models.CharField(max_length=10, choices=[
        ('always', 'Always'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('never', 'Never')
    ])
    lastmod = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.url