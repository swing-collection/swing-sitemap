from django.contrib.sitemaps.views import sitemap
from .sitemaps import MyModelSitemap

sitemaps = {
    'mymodel': MyModelSitemap,
}

# Sitemap Handlers
# =============================================================================

sitemaps = {
    # "static":   StaticViewSitemap,
    "views": StaticSitemap(STATIC_VIEWS),
    # "projects": GenericSitemap(
    #     {
    #         "queryset":     Project.objects.all(),
    #         "date_field":   "updated_date",
    #         },
    #         priority=0.9),
    # "stories": GenericSitemap(
    #     {
    #         "queryset":     Story.objects.all(),
    #         "date_field":   "updated_date",
    #         },
    #         priority=0.9),
}

urlpatterns = [
    # ... your other url patterns ...
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]





# sitemaps = {
#     'mymodel': MyModelSitemap,
# }

# urlpatterns = [
#     # ... your other url patterns ...
#     path('sitemap.xml', sitemap, {'sitemaps': sitemaps, 'template_name': 'custom_sitemap.xml'},
#          name='django.contrib.sitemaps.views.sitemap')
# ]


# from django.contrib.sitemaps.views import sitemap
# from .sitemaps import VideoSitemap

# sitemaps = {
#     'videos': VideoSitemap,
#     # ... other sitemaps ...
# }

# urlpatterns = [
#     # ... your other url patterns ...
#     path('sitemap_videos.xml', sitemap, {'sitemaps': sitemaps, 'template_name': 'custom_video_sitemap.xml'},
#          name='django.contrib.sitemaps.views.sitemap')
# ]



sitemaps = {
    'news': NewsSitemap,
    # ... other sitemaps ...
}

urlpatterns = [
    # ... your other url patterns ...
    path('sitemap_news
.xml', sitemap, {'sitemaps': sitemaps, 'template_name': 'custom_news_sitemap.xml'},
name='django.contrib.sitemaps.views.sitemap')
]