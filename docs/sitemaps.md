# Sitemap Classes

Swing Sitemap provides several sitemap classes for different content types.

## Overview

| Class           | Use Case               |
| --------------- | ---------------------- |
| `StaticSitemap` | Named Django views     |
| `ModelSitemap`  | Django model querysets |
| `VideoSitemap`  | Google Video sitemaps  |
| `NewsSitemap`   | Google News sitemaps   |
| `ImageSitemap`  | Image galleries        |
| `BaseSitemap`   | Custom implementations |

## StaticSitemap

For pages defined by Django URL names.

### Settings-Based

```python
# settings.py
SWING_SITEMAP = {
    "static": {
        "views": [
            "home",
            "about",
            "contact",
            {
                "view_name": "archive",
                "kwargs": {"year": 2024},
                "priority": 0.6,
            },
        ],
        "priority": 0.5,
        "changefreq": "monthly",
    },
}
```

### Code-Based

```python
from swing.sitemap import StaticSitemap

sitemap = StaticSitemap(
    views=[
        "home",
        "about",
        {"view_name": "blog:list", "priority": 0.8},
    ],
    priority=0.5,
    changefreq="weekly",
)

# In urls.py
sitemaps = {"static": sitemap}
```

### Custom StaticSitemap

```python
from swing.sitemap import StaticSitemap

class MyStaticSitemap(StaticSitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "about",
            "contact",
            {"view_name": "blog:archive", "kwargs": {"year": 2024}},
        ]

    def lastmod(self, item):
        # Custom lastmod logic
        if isinstance(item, dict) and item.get("view_name") == "home":
            return timezone.now()
        return None
```

## ModelSitemap

For Django model instances with URLs.

### Settings-Based

```python
SWING_SITEMAP = {
    "models": {
        "posts": {
            "model": "blog.Post",
            "filters": {"status": "published"},
            "order_by": ["-created_at"],
            "date_field": "updated_at",
            "priority": 0.8,
        },
    },
}
```

### Code-Based

```python
from swing.sitemap import ModelSitemap
from blog.models import Post

class PostSitemap(ModelSitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()
```

### Inline Construction

```python
from swing.sitemap import ModelSitemap
from blog.models import Post

sitemap = ModelSitemap(
    queryset=Post.objects.filter(status="published"),
    date_field="updated_at",
    priority=0.8,
    changefreq="daily",
)
```

### Advanced Model Sitemap

```python
from swing.sitemap import ModelSitemap

class ProductSitemap(ModelSitemap):
    limit = 10000  # Max items

    def items(self):
        return Product.objects.filter(
            active=True,
            stock__gt=0,
        ).select_related("category")

    def priority(self, obj):
        # Dynamic priority based on product
        if obj.featured:
            return 1.0
        if obj.category.slug == "sale":
            return 0.9
        return 0.7

    def changefreq(self, obj):
        if obj.category.slug == "sale":
            return "hourly"
        return "daily"
```

## VideoSitemap

For Google Video Sitemaps. See [Google Video Sitemap documentation](https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps).

### Basic Usage

```python
from swing.sitemap import VideoSitemap

class MyVideoSitemap(VideoSitemap):
    def items(self):
        return Video.objects.filter(published=True)

    # Required fields
    def video_title(self, obj):
        return obj.title

    def video_description(self, obj):
        return obj.description

    def video_thumbnail_loc(self, obj):
        return obj.thumbnail.url

    def video_content_loc(self, obj):
        return obj.video_file.url

    # Optional fields
    def video_duration(self, obj):
        return obj.duration  # In seconds

    def video_publication_date(self, obj):
        return obj.published_at

    def video_category(self, obj):
        return obj.category.name

    def video_family_friendly(self, obj):
        return obj.family_friendly  # "yes" or "no"
```

### Video Methods

| Method                             | Required | Description           |
| ---------------------------------- | -------- | --------------------- |
| `video_title(obj)`                 | Yes      | Video title           |
| `video_description(obj)`           | Yes      | Video description     |
| `video_thumbnail_loc(obj)`         | Yes      | Thumbnail URL         |
| `video_content_loc(obj)`           | \*       | Video file URL        |
| `video_player_loc(obj)`            | \*       | Embedded player URL   |
| `video_duration(obj)`              | No       | Duration in seconds   |
| `video_expiration_date(obj)`       | No       | Expiration date       |
| `video_rating(obj)`                | No       | Rating (0.0-5.0)      |
| `video_view_count(obj)`            | No       | View count            |
| `video_publication_date(obj)`      | No       | Publication date      |
| `video_family_friendly(obj)`       | No       | "yes" or "no"         |
| `video_category(obj)`              | No       | Category name         |
| `video_restriction(obj)`           | No       | Country restrictions  |
| `video_gallery_loc(obj)`           | No       | Gallery page URL      |
| `video_price(obj)`                 | No       | Price info            |
| `video_requires_subscription(obj)` | No       | "yes" or "no"         |
| `video_uploader(obj)`              | No       | Uploader name         |
| `video_live(obj)`                  | No       | "yes" or "no"         |
| `video_tag(obj)`                   | No       | Tags (list or string) |

\* Either `video_content_loc` or `video_player_loc` is required.

## NewsSitemap

For Google News Sitemaps. Articles must be published within the last 2 days.

### Basic Usage

```python
from swing.sitemap import NewsSitemap
from datetime import timedelta
from django.utils import timezone

class ArticleSitemap(NewsSitemap):
    publication_name = "My News Site"
    publication_language = "en"

    def items(self):
        # Only articles from the last 2 days
        cutoff = timezone.now() - timedelta(days=2)
        return Article.objects.filter(
            published_at__gte=cutoff,
            status="published",
        )

    def news_publication_date(self, obj):
        return obj.published_at

    def news_title(self, obj):
        return obj.headline

    # Optional
    def news_keywords(self, obj):
        return obj.keywords  # Comma-separated string

    def news_stock_tickers(self, obj):
        return obj.stock_tickers  # For financial news
```

### News Methods

| Method                       | Required | Description                |
| ---------------------------- | -------- | -------------------------- |
| `news_publication_date(obj)` | Yes      | Publication date           |
| `news_title(obj)`            | Yes      | Article title              |
| `news_keywords(obj)`         | No       | Keywords (comma-separated) |
| `news_stock_tickers(obj)`    | No       | Stock tickers              |

### Class Attributes

| Attribute              | Default  | Description             |
| ---------------------- | -------- | ----------------------- |
| `publication_name`     | Required | News publication name   |
| `publication_language` | `"en"`   | ISO 639-1 language code |

## ImageSitemap

For image-rich pages with multiple images.

```python
from swing.sitemap import ImageSitemap

class GallerySitemap(ImageSitemap):
    def items(self):
        return Gallery.objects.filter(published=True)

    def images(self, obj):
        """Return list of images for this gallery."""
        return [
            {
                "loc": img.url,
                "title": img.title,
                "caption": img.caption,
                "geo_location": img.location,
                "license": img.license_url,
            }
            for img in obj.images.all()
        ]
```

### Image Dict Keys

| Key            | Required | Description         |
| -------------- | -------- | ------------------- |
| `loc`          | Yes      | Image URL           |
| `title`        | No       | Image title         |
| `caption`      | No       | Image caption       |
| `geo_location` | No       | Geographic location |
| `license`      | No       | License URL         |

## HreflangMixin

For multi-language sites with alternate language versions.

```python
from swing.sitemap import ModelSitemap, HreflangMixin

class I18nPostSitemap(HreflangMixin, ModelSitemap):
    languages = ["en", "de", "fr", "es"]
    default_language = "en"

    def items(self):
        return Post.objects.filter(status="published")

    def alternates(self, obj):
        """Return dict of language -> URL."""
        return {
            lang: f"/{lang}/blog/{obj.slug}/"
            for lang in self.languages
            if obj.has_translation(lang)
        }

    def location(self, obj):
        return f"/{self.default_language}/blog/{obj.slug}/"
```

### With Django's i18n

```python
from django.urls import reverse
from django.utils.translation import activate

class I18nSitemap(HreflangMixin, ModelSitemap):
    languages = ["en", "de", "fr"]

    def alternates(self, obj):
        urls = {}
        for lang in self.languages:
            activate(lang)
            urls[lang] = reverse("blog:detail", kwargs={"slug": obj.slug})
        return urls
```

## BaseSitemap

Base class for fully custom sitemaps.

```python
from swing.sitemap import BaseSitemap

class CustomSitemap(BaseSitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        """Return items to include in sitemap."""
        return ["item1", "item2", "item3"]

    def location(self, item):
        """Return URL for item."""
        return f"/custom/{item}/"

    def lastmod(self, item):
        """Return last modification date."""
        return None

    def priority(self, item):
        """Return priority (0.0-1.0)."""
        return 0.5

    def changefreq(self, item):
        """Return change frequency."""
        return "weekly"
```

## Composing Sitemaps

### Manual Composition

```python
from swing.sitemap import StaticSitemap, ModelSitemap

sitemaps = {
    "static": StaticSitemap(views=["home", "about"]),
    "posts": PostSitemap,
    "products": ProductSitemap,
}
```

### With default_sitemaps()

```python
from swing.sitemap import default_sitemaps

# Get sitemaps from settings
sitemaps = default_sitemaps()

# Add custom sitemaps
sitemaps["videos"] = VideoSitemap
sitemaps["news"] = ArticleSitemap
```

### With Wagtail

```python
from swing.sitemap import default_sitemaps, sitemap_urlpatterns
from wagtail.contrib.sitemaps import Sitemap as WagtailSitemap

sitemaps = {
    **default_sitemaps(),
    "wagtail": WagtailSitemap,
}

urlpatterns = [
    *sitemap_urlpatterns(sitemaps=sitemaps),
]
```

## Pagination

For large sitemaps, use `PaginatedSitemap`:

```python
from swing.sitemap import PaginatedSitemap, ModelSitemap

class LargePostSitemap(ModelSitemap):
    limit = None  # No limit

    def items(self):
        return Post.objects.all()  # 100,000+ items

# Wrap with pagination
paginated = PaginatedSitemap(
    LargePostSitemap,
    items_per_page=10000,
)
```

Or enable globally in settings:

```python
SWING_SITEMAP = {
    "pagination": {
        "enabled": True,
        "items_per_page": 10000,
    },
}
```
