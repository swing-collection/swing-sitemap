from django.shortcuts import render
from django.http import HttpResponse
from .sitemaps import NewsSitemap

def news_sitemap(request):
    sitemap = NewsSitemap()
    urls = sitemap.get_urls()
    return render(request, 'sitemap_news.xml', {'urlset': urls}, content_type='application/xml')