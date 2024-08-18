from django.shortcuts import render
from django.http import HttpResponse
from .sitemaps import ImageSitemap

def image_sitemap(request):
    sitemap = ImageSitemap()
    urls = sitemap.get_urls()
    return render(request, 'sitemap_image.xml', {'urlset': urls}, content_type='application/xml')