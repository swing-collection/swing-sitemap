<p align="center">
    <img src="https://github.com/scape-agency/swing.dj/blob/85830584264bca52c02e1f0dcfa3648f84783805/res/swing-logo.png" width="20%" height="20%" alt="Django Swing Logo">
</p>
<h1 align='center' style='border-bottom: none;'>Swing Sitemap</h1>
<h3 align='center'>Django Swing Collection</h3>

<p align="center">
    <a href="https://pypi.org/project/swing-sitemap/"><img src="https://img.shields.io/pypi/v/swing-sitemap.svg" alt="PyPI"></a>
    <a href="https://pypi.org/project/swing-sitemap/"><img src="https://img.shields.io/pypi/pyversions/swing-sitemap.svg" alt="Python versions"></a>
    <a href="https://github.com/swing-collection/swing-sitemap/blob/dev/LICENSE"><img src="https://img.shields.io/badge/license-BSD--3--Clause-blue.svg" alt="License"></a>
    <a href="https://github.com/swing-collection/swing-sitemap/actions"><img src="https://github.com/swing-collection/swing-sitemap/workflows/CI/badge.svg" alt="CI Status"></a>
</p>

---

## Overview

**Swing Sitemap** is a powerful, CMS-agnostic Django app that extends `django.contrib.sitemaps` with a settings-driven, drop-in URL helper and versatile sitemap classes. It eliminates the boilerplate of `sitemaps.py` + `urls.py` wiring, reducing setup to just a few import lines.

### Features

| Feature                      | Description                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------------------- |
| **StaticSitemap**            | Sitemap of named Django views with support for `view_name`, `args`, `kwargs`, and `lastmod` |
| **ModelSitemap**             | Generic queryset adapter for any Django model                                               |
| **VideoSitemap**             | Google Video sitemap with full video metadata support                                       |
| **NewsSitemap**              | Google News sitemap for news articles                                                       |
| **ImageSitemap**             | Image sitemap with gallery support                                                          |
| **HreflangMixin**            | Multi-language support with `hreflang` alternate links                                      |
| **Pagination**               | Automatic pagination for large sitemaps (50,000 URLs limit)                                 |
| **Caching**                  | Built-in cache support with configurable TTL                                                |
| **Compression**              | Gzip compression for sitemap responses                                                      |
| **Signals**                  | Auto-invalidate cache on model changes                                                      |
| **Search Engine Submission** | Ping Google, Bing, and custom endpoints                                                     |
| **Management Commands**      | CLI tools for generation, validation, and submission                                        |

## Requirements

- Python 3.12+
- Django 5.0+ / 6.0+

## Installation

```bash
pip install swing-sitemap
```

Or with Poetry:

```bash
poetry add swing-sitemap
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "django.contrib.sitemaps",
    "swing.sitemap",
]
```

## Quick Start

### 1. Configure Settings

```python
# settings.py
SWING_SITEMAP = {
    # Static pages sitemap
    "static": {
        "views": ["home", "about", "contact"],
        "priority": 0.6,
        "changefreq": "weekly",
    },
    # Model-based sitemaps
    "models": {
        "blog": {
            "model": "blog.Post",
            "filters": {"is_published": True},
            "order_by": ["-published_at"],
            "date_field": "updated_at",
            "priority": 0.8,
            "changefreq": "daily",
        },
        "products": {
            "model": "shop.Product",
            "filters": {"active": True},
            "priority": 0.7,
        },
    },
    # Caching (optional)
    "cache": {
        "enabled": True,
        "timeout": 3600,  # 1 hour
        "key_prefix": "sitemap",
    },
    # Pagination (optional)
    "pagination": {
        "enabled": True,
        "items_per_page": 10000,
    },
}
```

### 2. Wire URLs

```python
# urls.py
from swing.sitemap.urls import sitemap_urlpatterns

urlpatterns = [
    # ... your views ...
    *sitemap_urlpatterns(),
]
```

That's it! Your sitemap is now available at `/sitemap.xml`.

### 3. Add to robots.txt (Optional)

```python
# settings.py
TEMPLATES = [
    {
        # ...
        "OPTIONS": {
            "context_processors": [
                # ...
                "swing.sitemap.context_processors.sitemap_url",
            ],
        },
    },
]
```

```text
# templates/robots.txt
Sitemap: {{ sitemap_url }}
```

Or use the template tag:

```django
{% load swing_sitemap %}
Sitemap: {% sitemap_url %}
```

## Sitemap Classes

### StaticSitemap

For named Django views:

```python
from swing.sitemap import StaticSitemap

sitemap = StaticSitemap(
    views=["home", "about", {"view_name": "blog:archive", "kwargs": {"year": 2024}}],
    priority=0.8,
    changefreq="weekly",
)
```

### ModelSitemap

For Django model querysets:

```python
from swing.sitemap import ModelSitemap
from blog.models import Post

sitemap = ModelSitemap(
    queryset=Post.objects.filter(is_published=True),
    date_field="updated_at",
    priority=0.7,
)
```

### VideoSitemap

For video content (Google Video Sitemaps):

```python
from swing.sitemap import VideoSitemap

class MyVideoSitemap(VideoSitemap):
    def items(self):
        return Video.objects.filter(published=True)

    def video_title(self, obj):
        return obj.title

    def video_description(self, obj):
        return obj.description

    def video_thumbnail_loc(self, obj):
        return obj.thumbnail.url
```

### NewsSitemap

For news articles (Google News Sitemaps):

```python
from swing.sitemap import NewsSitemap

class MyNewsSitemap(NewsSitemap):
    publication_name = "My News Site"
    publication_language = "en"

    def items(self):
        return Article.objects.filter(
            published_at__gte=timezone.now() - timedelta(days=2)
        )
```

### HreflangMixin

For multi-language sites:

```python
from swing.sitemap import ModelSitemap, HreflangMixin

class I18nBlogSitemap(HreflangMixin, ModelSitemap):
    languages = ["en", "de", "fr"]

    def alternates(self, obj):
        return {
            lang: f"/{lang}/blog/{obj.slug}/"
            for lang in self.languages
        }
```

## Management Commands

### Generate Static Sitemap

```bash
python manage.py generate_sitemap --output sitemap.xml
```

### Validate Sitemap

```bash
# Validate from URL
python manage.py validate_sitemap https://example.com/sitemap.xml

# Validate all configured sitemaps
python manage.py validate_sitemap --all
```

### Submit to Search Engines

```bash
python manage.py submit_sitemap https://example.com/sitemap.xml
```

### Clear Sitemap Cache

```bash
python manage.py clear_sitemap_cache
```

## Celery Tasks (Optional)

For async sitemap submission:

```python
# settings.py
SWING_SITEMAP = {
    "submit": {
        "sitemap_url": "https://example.com/sitemap.xml",
        "endpoints": {
            "google": "https://www.google.com/ping?sitemap={url}",
            "bing": "https://www.bing.com/ping?sitemap={url}",
        },
    },
}
```

```python
# tasks.py
from swing.sitemap.tasks import submit_sitemap_task

# Submit immediately
submit_sitemap_task.delay()
```

## Composing Extra Sitemaps

Swing Sitemap is CMS-agnostic. Integrate with Wagtail or other CMSes:

```python
from swing.sitemap import default_sitemaps, sitemap_urlpatterns
from wagtail.contrib.sitemaps import Sitemap as WagtailSitemap

sitemaps = {**default_sitemaps(), "wagtail": WagtailSitemap}

urlpatterns = [
    *sitemap_urlpatterns(sitemaps=sitemaps),
]
```

## Configuration Reference

| Setting                     | Type    | Default           | Description                      |
| --------------------------- | ------- | ----------------- | -------------------------------- |
| `static.views`              | `list`  | `[]`              | List of view names or dicts      |
| `static.priority`           | `float` | `0.5`             | Default priority for static URLs |
| `static.changefreq`         | `str`   | `"monthly"`       | Default change frequency         |
| `models.<key>.model`        | `str`   | Required          | Model path (e.g., `"app.Model"`) |
| `models.<key>.filters`      | `dict`  | `{}`              | Queryset filter kwargs           |
| `models.<key>.order_by`     | `list`  | `[]`              | Ordering fields                  |
| `models.<key>.date_field`   | `str`   | `None`            | Field for lastmod                |
| `models.<key>.priority`     | `float` | `0.5`             | URL priority (0.0-1.0)           |
| `models.<key>.changefreq`   | `str`   | `"monthly"`       | Change frequency                 |
| `cache.enabled`             | `bool`  | `False`           | Enable sitemap caching           |
| `cache.timeout`             | `int`   | `3600`            | Cache TTL in seconds             |
| `cache.key_prefix`          | `str`   | `"swing_sitemap"` | Cache key prefix                 |
| `pagination.enabled`        | `bool`  | `False`           | Enable pagination                |
| `pagination.items_per_page` | `int`   | `50000`           | URLs per sitemap page            |
| `compression.enabled`       | `bool`  | `False`           | Enable gzip compression          |

## Signals

Automatically invalidate cache when models change:

```python
# apps.py
from django.apps import AppConfig

class BlogConfig(AppConfig):
    def ready(self):
        from swing.sitemap import register_sitemap_signals
        from .models import Post

        register_sitemap_signals(Post)
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

```bash
# Clone the repository
git clone https://github.com/swing-collection/swing-sitemap.git
cd swing-sitemap

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linters
poetry run flake8 src/
poetry run pylint src/
```

## License

This project is licensed under the BSD-3-Clause License. See [LICENSE](LICENSE) for details.

## Links

- **Documentation**: [https://swing.dj/](https://swing.dj/)
- **Repository**: [https://github.com/swing-collection/swing-sitemap](https://github.com/swing-collection/swing-sitemap)
- **PyPI**: [https://pypi.org/project/swing-sitemap/](https://pypi.org/project/swing-sitemap/)
- **Issues**: [https://github.com/swing-collection/swing-sitemap/issues](https://github.com/swing-collection/swing-sitemap/issues)

### `robots.txt`

Use the template tag or context processor:

```django
{% load swing_sitemap %}
Sitemap: {% sitemap_url %}
```

Or enable the context processor and reference `{{ SITEMAP_URL }}`:

```python
TEMPLATES = [{
    "OPTIONS": {
        "context_processors": [
            # ...
            "swing_sitemap.context_processors.sitemap_url",
        ],
    },
}]
```

## Settings reference

| Key                          | Default              | Notes                                                                |
| ---------------------------- | -------------------- | -------------------------------------------------------------------- |
| `static.views`               | `[]`                 | List of URL names or `{view_name, args, kwargs, lastmod}` dicts.     |
| `static.priority`            | `0.5`                | Default `<priority>` for every static entry.                         |
| `static.changefreq`          | `"monthly"`          | Default `<changefreq>` for every static entry.                       |
| `models.<key>.model`         | required             | Dotted `"app.Model"`.                                                |
| `models.<key>.filters`       | `{}`                 | `**filters` passed to `qs.filter()`.                                 |
| `models.<key>.exclude`       | `{}`                 | `**filters` passed to `qs.exclude()`.                                |
| `models.<key>.order_by`      | `[]`                 | Args passed to `qs.order_by()`.                                      |
| `models.<key>.date_field`    | `None`               | Attribute used for `<lastmod>`.                                      |
| `models.<key>.location_attr` | `"get_absolute_url"` | Attribute or zero-arg callable returning the URL.                    |
| `models.<key>.priority`      | `None`               | Per-sitemap `<priority>`.                                            |
| `models.<key>.changefreq`    | `None`               | Per-sitemap `<changefreq>`.                                          |
| `priority` / `changefreq`    | `{}`                 | Free-form per-key dicts (legacy `SEO_SITEMAP_*` shims fold in here). |

### Backward-compatibility shims

The following legacy settings still work but emit a `DeprecationWarning`
the first time `get_config()` runs:

- `SEO_SITEMAP_PRIORITY` → `SWING_SITEMAP["priority"]`
- `SEO_SITEMAP_CHANGEFREQ` → `SWING_SITEMAP["changefreq"]`
- `VIDEO_SITEMAP_MODEL` → `SWING_SITEMAP["video"]["model"]`

## Testing

```bash
poetry install --with dev
poetry run pytest
```

---

## Colophon

Made with ❤️ by **[Scape Press](https://www.scape.press)**

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

### License

This project is licensed under the BSD-3-Clause license. See the [LICENSE](LICENSE) file for details.

---
