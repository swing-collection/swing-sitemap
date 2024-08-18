# swing_sitemap/views.py
from django.http import HttpResponse
from django.template import loader

def sitemap_index(request):
    sitemaps = [
        'sitemap.xml',
        'image_sitemap.xml',
        'video_sitemap.xml',
        'news_sitemap.xml'
    ]
    template = loader.get_template('swing_sitemap/sitemap_index.xml')
    context = {'sitemaps': sitemaps}
    return HttpResponse(template.render(context), content_type='application/xml')