# Swing Sitemap

**A powerful, CMS-agnostic Django sitemap toolkit.**

Swing Sitemap extends Django's built-in sitemap framework with a settings-driven approach, eliminating boilerplate while adding powerful features like video sitemaps, news sitemaps, multi-language support, caching, and automatic pagination.

## Why Swing Sitemap?

- **Zero Boilerplate** — Configure sitemaps in settings, not code
- **CMS-Agnostic** — Works with Django, Wagtail, or any CMS
- **Feature-Rich** — Video, News, Image sitemaps out of the box
- **Production-Ready** — Built-in caching, compression, and pagination
- **Search Engine Friendly** — Auto-submit to Google, Bing, and more

## Installation

```bash
pip install swing-sitemap
```

```python
# settings.py
INSTALLED_APPS = [
    "django.contrib.sitemaps",
    "swing.sitemap",
]
```

## Quick Example

```python
# settings.py
SWING_SITEMAP = {
    "static": {
        "views": ["home", "about", "contact"],
    },
    "models": {
        "blog": {
            "model": "blog.Post",
            "filters": {"is_published": True},
        },
    },
}

# urls.py
from swing.sitemap.urls import sitemap_urlpatterns
urlpatterns = [..., *sitemap_urlpatterns()]
```

Your sitemap is now live at `/sitemap.xml`.

## Documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Quick Start](quick_start.md)**

    Get up and running in 5 minutes

- :material-cog: **[Configuration](configuration.md)**

    Complete settings reference

- :material-sitemap: **[Sitemap Classes](sitemaps.md)**

    StaticSitemap, ModelSitemap, VideoSitemap, and more

- :material-console: **[Management Commands](commands.md)**

    CLI tools for generation, validation, and submission

</div>

## Features

### Sitemap Types

| Type              | Description                 |
| ----------------- | --------------------------- |
| **StaticSitemap** | Named Django views          |
| **ModelSitemap**  | Any Django model queryset   |
| **VideoSitemap**  | Google Video sitemap format |
| **NewsSitemap**   | Google News sitemap format  |
| **ImageSitemap**  | Image galleries and media   |

### Core Features

- **Pagination** — Automatic splitting for large sitemaps (50,000 URL limit)
- **Caching** — Configurable cache with TTL and auto-invalidation
- **Compression** — Gzip support for faster delivery
- **Multi-language** — `HreflangMixin` for internationalized sites
- **Signals** — Auto-refresh cache when content changes

### Management Commands

```bash
# Generate static XML file
python manage.py generate_sitemap --output sitemap.xml

# Validate sitemap structure
python manage.py validate_sitemap --all

# Submit to search engines
python manage.py submit_sitemap https://example.com/sitemap.xml

# Clear sitemap cache
python manage.py clear_sitemap_cache
```

## Requirements

- Python 3.12+
- Django 5.0+ or 6.0+

## License

BSD-3-Clause — see [LICENSE](https://github.com/swing-collection/swing-sitemap/blob/dev/LICENSE)
