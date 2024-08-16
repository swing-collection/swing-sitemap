from django.contrib import admin
from .models import StandardSitemapURL, ImageSitemapURL, VideoSitemapURL, NewsSitemapURL, CustomSitemapURL

admin.site.register(StandardSitemapURL)
admin.site.register(ImageSitemapURL)
admin.site.register(VideoSitemapURL)
admin.site.register(NewsSitemapURL)
admin.site.register(CustomSitemapURL)