# Configuration Reference

Complete reference for the `SWING_SITEMAP` settings dictionary.

## Basic Structure

```python
SWING_SITEMAP = {
    "static": {...},      # Static page sitemap config
    "models": {...},      # Model-based sitemap configs
    "cache": {...},       # Caching settings
    "pagination": {...},  # Pagination settings
    "compression": {...}, # Compression settings
    "submit": {...},      # Search engine submission
}
```

## Static Sitemap

Configure a sitemap for named Django views.

```python
SWING_SITEMAP = {
    "static": {
        "views": [
            "home",                              # Simple view name
            "about",
            {"view_name": "contact"},            # Dict format
            {
                "view_name": "blog:archive",
                "kwargs": {"year": 2024},
                "priority": 0.6,
            },
        ],
        "priority": 0.5,        # Default priority (0.0-1.0)
        "changefreq": "monthly", # Default change frequency
    },
}
```

### View Entry Options

| Key          | Type       | Description                 |
| ------------ | ---------- | --------------------------- |
| `view_name`  | `str`      | Django URL name (required)  |
| `args`       | `list`     | Positional URL arguments    |
| `kwargs`     | `dict`     | Keyword URL arguments       |
| `priority`   | `float`    | Override priority (0.0-1.0) |
| `changefreq` | `str`      | Override change frequency   |
| `lastmod`    | `datetime` | Last modification date      |

### Change Frequencies

Valid values: `"always"`, `"hourly"`, `"daily"`, `"weekly"`, `"monthly"`, `"yearly"`, `"never"`

## Model Sitemaps

Configure sitemaps from Django model querysets.

```python
SWING_SITEMAP = {
    "models": {
        "blog": {
            "model": "blog.Post",
            "filters": {"status": "published", "is_public": True},
            "exclude": {"featured": True},
            "order_by": ["-published_at"],
            "date_field": "updated_at",
            "location_attr": "get_absolute_url",
            "priority": 0.8,
            "changefreq": "weekly",
            "limit": 10000,
            "protocol": "https",
        },
        "products": {
            "model": "shop.Product",
            "filters": {"active": True},
            "priority": 0.7,
        },
    },
}
```

### Model Options

| Key             | Type    | Default              | Description                 |
| --------------- | ------- | -------------------- | --------------------------- |
| `model`         | `str`   | Required             | Model path as `"app.Model"` |
| `filters`       | `dict`  | `{}`                 | `filter()` kwargs           |
| `exclude`       | `dict`  | `{}`                 | `exclude()` kwargs          |
| `order_by`      | `list`  | `[]`                 | `order_by()` fields         |
| `date_field`    | `str`   | `None`               | Field for `lastmod`         |
| `location_attr` | `str`   | `"get_absolute_url"` | Method/attribute for URL    |
| `priority`      | `float` | `0.5`                | URL priority (0.0-1.0)      |
| `changefreq`    | `str`   | `"monthly"`          | Change frequency            |
| `limit`         | `int`   | `None`               | Max items to include        |
| `protocol`      | `str`   | `"https"`            | URL protocol                |

## Cache Settings

```python
SWING_SITEMAP = {
    "cache": {
        "enabled": True,
        "backend": "default",           # Django cache backend name
        "timeout": 3600,                # TTL in seconds (1 hour)
        "key_prefix": "swing_sitemap",  # Cache key prefix
    },
}
```

### Cache Options

| Key          | Type   | Default           | Description          |
| ------------ | ------ | ----------------- | -------------------- |
| `enabled`    | `bool` | `False`           | Enable caching       |
| `backend`    | `str`  | `"default"`       | Django cache backend |
| `timeout`    | `int`  | `3600`            | Cache TTL in seconds |
| `key_prefix` | `str`  | `"swing_sitemap"` | Cache key prefix     |

## Pagination Settings

For large sitemaps exceeding the 50,000 URL limit.

```python
SWING_SITEMAP = {
    "pagination": {
        "enabled": True,
        "items_per_page": 10000,
    },
}
```

### Pagination Options

| Key              | Type   | Default | Description           |
| ---------------- | ------ | ------- | --------------------- |
| `enabled`        | `bool` | `False` | Enable pagination     |
| `items_per_page` | `int`  | `50000` | URLs per sitemap page |

When enabled, the sitemap index (`/sitemap.xml`) links to paginated sitemaps (`/sitemap-1.xml`, `/sitemap-2.xml`, etc.).

## Compression Settings

```python
SWING_SITEMAP = {
    "compression": {
        "enabled": True,
    },
}
```

### Compression Options

| Key       | Type   | Default | Description             |
| --------- | ------ | ------- | ----------------------- |
| `enabled` | `bool` | `False` | Enable gzip compression |

## Search Engine Submission

Configure automatic sitemap submission to search engines.

```python
SWING_SITEMAP = {
    "submit": {
        "sitemap_url": "https://example.com/sitemap.xml",
        "endpoints": {
            "google": "https://www.google.com/ping?sitemap={url}",
            "bing": "https://www.bing.com/ping?sitemap={url}",
        },
        "timeout": 10.0,
        "retry_delay": 60,
        "max_retries": 3,
    },
}
```

### Submit Options

| Key           | Type    | Default      | Description                |
| ------------- | ------- | ------------ | -------------------------- |
| `sitemap_url` | `str`   | None         | Absolute URL of sitemap    |
| `endpoints`   | `dict`  | Google, Bing | Ping endpoint URLs         |
| `timeout`     | `float` | `10.0`       | Request timeout in seconds |
| `retry_delay` | `int`   | `60`         | Retry delay in seconds     |
| `max_retries` | `int`   | `3`          | Maximum retry attempts     |

## Signal Settings

Configure automatic cache invalidation on model changes.

```python
SWING_SITEMAP = {
    "signals": {
        "enabled": True,
        "debounce_seconds": 5,  # Batch rapid changes
        "submit_on_change": False,  # Auto-submit after invalidation
    },
}
```

## Priority and Changefreq Overrides

Override defaults per sitemap section:

```python
SWING_SITEMAP = {
    "priority": {
        "blog": 0.8,
        "products": 0.7,
        "static": 0.5,
    },
    "changefreq": {
        "blog": "daily",
        "products": "weekly",
        "static": "monthly",
    },
}
```

## Full Example

```python
SWING_SITEMAP = {
    # Static pages
    "static": {
        "views": ["home", "about", "contact", "privacy", "terms"],
        "priority": 0.5,
        "changefreq": "monthly",
    },

    # Model sitemaps
    "models": {
        "blog": {
            "model": "blog.Post",
            "filters": {"status": "published"},
            "order_by": ["-published_at"],
            "date_field": "updated_at",
            "priority": 0.8,
            "changefreq": "daily",
        },
        "categories": {
            "model": "blog.Category",
            "filters": {"active": True},
            "priority": 0.4,
            "changefreq": "weekly",
        },
    },

    # Performance
    "cache": {
        "enabled": True,
        "timeout": 3600,
    },
    "pagination": {
        "enabled": True,
        "items_per_page": 25000,
    },
    "compression": {
        "enabled": True,
    },

    # Search engine submission
    "submit": {
        "sitemap_url": "https://example.com/sitemap.xml",
    },
}
```

## Environment-Specific Config

```python
# settings/base.py
SWING_SITEMAP = {
    "static": {"views": ["home", "about"]},
    "models": {"blog": {"model": "blog.Post"}},
}

# settings/production.py
SWING_SITEMAP = {
    **SWING_SITEMAP,
    "cache": {"enabled": True, "timeout": 7200},
    "compression": {"enabled": True},
    "submit": {"sitemap_url": "https://example.com/sitemap.xml"},
}
```

## Programmatic Access

```python
from swing.sitemap import get_config, get_setting

# Get full config
config = get_config()

# Get specific setting with default
cache_timeout = get_setting("cache.timeout", default=3600)
```
