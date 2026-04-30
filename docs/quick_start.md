# Quick Start

Get Swing Sitemap running in your Django project in under 5 minutes.

## Installation

### Using pip

```bash
pip install swing-sitemap
```

### Using Poetry

```bash
poetry add swing-sitemap
```

## Configuration

### 1. Add to INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    # Django core
    "django.contrib.sites",
    "django.contrib.sitemaps",

    # Swing Sitemap
    "swing.sitemap",

    # Your apps
    "blog",
    "shop",
]

SITE_ID = 1
```

### 2. Configure Your Sitemaps

Add the `SWING_SITEMAP` setting:

```python
# settings.py
SWING_SITEMAP = {
    # Static pages (views by name)
    "static": {
        "views": [
            "home",
            "about",
            "contact",
            {"view_name": "faq", "priority": 0.3},
        ],
        "priority": 0.5,
        "changefreq": "monthly",
    },

    # Model-based sitemaps
    "models": {
        "blog": {
            "model": "blog.Post",
            "filters": {"status": "published"},
            "order_by": ["-published_at"],
            "date_field": "updated_at",
            "priority": 0.8,
            "changefreq": "weekly",
        },
        "products": {
            "model": "shop.Product",
            "filters": {"active": True},
            "priority": 0.7,
            "changefreq": "daily",
        },
    },
}
```

### 3. Wire the URLs

```python
# urls.py
from django.urls import path, include
from swing.sitemap.urls import sitemap_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),

    # Add sitemap URLs
    *sitemap_urlpatterns(),
]
```

### 4. Test It

Start your development server and visit:

- `http://localhost:8000/sitemap.xml` — Your sitemap

## Adding to robots.txt

### Option 1: Context Processor

```python
# settings.py
TEMPLATES = [
    {
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
User-agent: *
Allow: /

Sitemap: {{ sitemap_url }}
```

### Option 2: Template Tag

```django
{% load swing_sitemap %}

User-agent: *
Allow: /

Sitemap: {% sitemap_url %}
```

## Model Requirements

For `ModelSitemap` to work, your models should have:

### get_absolute_url()

```python
# models.py
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    # ...

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"
```

### Optional: Date Field

For `lastmod` in the sitemap, specify a date field:

```python
SWING_SITEMAP = {
    "models": {
        "blog": {
            "model": "blog.Post",
            "date_field": "updated_at",  # or "modified_at", "published_at"
        },
    },
}
```

## Enabling Features

### Caching

```python
SWING_SITEMAP = {
    # ...
    "cache": {
        "enabled": True,
        "timeout": 3600,  # 1 hour
    },
}
```

### Pagination

For sitemaps with more than 50,000 URLs:

```python
SWING_SITEMAP = {
    # ...
    "pagination": {
        "enabled": True,
        "items_per_page": 10000,
    },
}
```

### Compression

```python
SWING_SITEMAP = {
    # ...
    "compression": {
        "enabled": True,
    },
}
```

## Next Steps

- [Configuration Reference](configuration.md) — All available settings
- [Sitemap Classes](sitemaps.md) — VideoSitemap, NewsSitemap, custom sitemaps
- [Management Commands](commands.md) — CLI tools for validation and submission
