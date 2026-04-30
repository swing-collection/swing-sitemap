from django.shortcuts import render
from django.http import HttpResponse
from .sitemaps import StaticSitemap

def static_sitemap(request):
    sitemap = StaticSitemap()
    urls = sitemap.get_urls()
    return render(request, 'sitemap_static.xml', {'urlset': urls}, content_type='application/xml')