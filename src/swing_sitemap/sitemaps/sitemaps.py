from django.contrib.sitemaps import Sitemap
from .models import MyModel

class MyModelSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return MyModel.objects.all()

    def lastmod(self, obj):
        return obj.modified_date
