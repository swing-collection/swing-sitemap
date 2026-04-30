<p align="center">
    <img src="https://github.com/scape-agency/swing.dj/blob/85830584264bca52c02e1f0dcfa3648f84783805/res/swing-logo.png" width="20%" height="20%" alt="Django Swing Logo">
</p>
<h1 align='center' style='border-bottom: none;'>Sitemap Swing</h1>
<h3 align='center'>Django Swing Collection</h3>
<br/>


---

## Overview

`swing_sitemap` is a small, CMS-agnostic Django app that wraps
`django.contrib.sitemaps` with a settings-driven, drop-in URL helper and
a couple of generic sitemap classes. The goal is to collapse the
boilerplate `sitemaps.py` + `urls.py` wiring used across the scapepress
sites into one or two import lines.

Highlights:

- **`StaticSitemap`** — sitemap of named Django views; entries are URL
  name strings *or* dicts with `view_name`, `args`, `kwargs`, `lastmod`.
- **`ModelSitemap`** — generic queryset adapter; constructed inline or
  declaratively from `SWING_SITEMAP["models"][key]`.
- **`default_sitemaps()`** — canonical `sitemaps` dict combining the
  static entry and one `ModelSitemap` per configured model. CMS-agnostic
  by design; sites that need Wagtail merge their own entry in.
- **`sitemap_urlpatterns()`** — registers `/sitemap.xml` and (optionally)
  the index + per-section URLs in one line.
- **`{% sitemap_url %}` template tag + context processor** — for use in
  `robots.txt` templates.
- **`submit_sitemap()`** — pings search engine endpoints.

## Quickstart

Install and add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "django.contrib.sitemaps",
    "swing_sitemap",
]
```

Configure (single namespace; all keys optional):

```python
SWING_SITEMAP = {
    "static": {
        "views": ["home", {"view_name": "about"}],
        "priority": 0.6,
        "changefreq": "weekly",
    },
    "models": {
        "work": {
            "model": "myapp.Work",
            "filters": {"is_published": True},
            "order_by": ["-work_date"],
            "date_field": "modified_at",
            "location_attr": "get_absolute_url",
            "priority": 0.8,
            "changefreq": "weekly",
        },
    },
}
```

Wire into your project URLs:

```python
# project/urls.py
from swing_sitemap.urls import sitemap_urlpatterns

urlpatterns = [
    # ... your views ...
    *sitemap_urlpatterns(),                       # /sitemap.xml
    # or, for a per-section index:
    # *sitemap_urlpatterns(include_index=True),   # /sitemap-index.xml + /sitemap-<section>.xml
]
```

That's it — `/sitemap.xml` returns a valid `<urlset>` driven by your
settings.

### Composing extra sitemaps (e.g. Wagtail)

`swing_sitemap` is intentionally CMS-agnostic. Sites that want a Wagtail
page sitemap merge it themselves:

```python
from swing_sitemap import default_sitemaps, sitemap_urlpatterns
from wagtail.contrib.sitemaps import Sitemap as WagtailSitemap

sitemaps = {**default_sitemaps(), "wagtail": WagtailSitemap}

urlpatterns = [
    *sitemap_urlpatterns(sitemaps=sitemaps),
]
```

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

| Key                        | Default                                          | Notes                                                                 |
| -------------------------- | ------------------------------------------------ | --------------------------------------------------------------------- |
| `static.views`             | `[]`                                             | List of URL names or `{view_name, args, kwargs, lastmod}` dicts.      |
| `static.priority`          | `0.5`                                            | Default `<priority>` for every static entry.                          |
| `static.changefreq`        | `"monthly"`                                      | Default `<changefreq>` for every static entry.                        |
| `models.<key>.model`       | required                                         | Dotted `"app.Model"`.                                                 |
| `models.<key>.filters`     | `{}`                                             | `**filters` passed to `qs.filter()`.                                  |
| `models.<key>.exclude`     | `{}`                                             | `**filters` passed to `qs.exclude()`.                                 |
| `models.<key>.order_by`    | `[]`                                             | Args passed to `qs.order_by()`.                                       |
| `models.<key>.date_field`  | `None`                                           | Attribute used for `<lastmod>`.                                       |
| `models.<key>.location_attr` | `"get_absolute_url"`                           | Attribute or zero-arg callable returning the URL.                     |
| `models.<key>.priority`    | `None`                                           | Per-sitemap `<priority>`.                                             |
| `models.<key>.changefreq`  | `None`                                           | Per-sitemap `<changefreq>`.                                           |
| `priority` / `changefreq`  | `{}`                                             | Free-form per-key dicts (legacy `SEO_SITEMAP_*` shims fold in here).  |

### Backward-compatibility shims

The following legacy settings still work but emit a `DeprecationWarning`
the first time `get_config()` runs:

- `SEO_SITEMAP_PRIORITY`   → `SWING_SITEMAP["priority"]`
- `SEO_SITEMAP_CHANGEFREQ` → `SWING_SITEMAP["changefreq"]`
- `VIDEO_SITEMAP_MODEL`    → `SWING_SITEMAP["video"]["model"]`

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
