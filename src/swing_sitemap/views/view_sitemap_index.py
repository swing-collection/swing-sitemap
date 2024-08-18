from django.shortcuts import render
from django.http import HttpResponse
from .sitemaps import StaticSitemap, ImageSitemap, VideoSitemap, NewsSitemap

def sitemap_index(request):
    sitemaps = [
        {'location': '/sitemap_static.xml', 'lastmod': '2024-08-01'},
        {'location': '/sitemap_images.xml', 'lastmod': '2024-08-02'},
        {'location': '/sitemap_videos.xml', 'lastmod': '2024-08-03'},
        {'location': '/sitemap_news.xml', 'lastmod': '2024-08-04'},
    ]
    return render(request, 'sitemap_index.xml', {'sitemapindex': sitemaps}, content_type='application/xml')