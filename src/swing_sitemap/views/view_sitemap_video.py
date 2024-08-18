from django.shortcuts import render
from django.http import HttpResponse
from .sitemaps import VideoSitemap

def video_sitemap(request):
    sitemap = VideoSitemap()
    urls = sitemap.get_urls()
    return render(request, 'sitemap_video.xml', {'urlset': urls}, content_type='application/xml')