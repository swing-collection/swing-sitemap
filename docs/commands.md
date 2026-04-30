# Management Commands

Swing Sitemap provides CLI tools for generating, validating, and submitting sitemaps.

## Overview

| Command               | Description                         |
| --------------------- | ----------------------------------- |
| `generate_sitemap`    | Generate static XML sitemap files   |
| `validate_sitemap`    | Validate sitemap structure and URLs |
| `submit_sitemap`      | Submit sitemap to search engines    |
| `clear_sitemap_cache` | Clear cached sitemap data           |

## generate_sitemap

Generate static XML sitemap files for deployment or CDN hosting.

### Basic Usage

```bash
# Generate to stdout
python manage.py generate_sitemap

# Generate to file
python manage.py generate_sitemap --output sitemap.xml

# Generate to directory (for large sitemaps)
python manage.py generate_sitemap --output-dir ./sitemaps/
```

### Options

| Option           | Description                             |
| ---------------- | --------------------------------------- |
| `--output`, `-o` | Output file path                        |
| `--output-dir`   | Output directory for multiple files     |
| `--format`       | Output format: `xml` (default) or `txt` |
| `--compress`     | Gzip compress output files              |
| `--section`      | Generate only specific section          |
| `--limit`        | Max URLs per file                       |
| `--base-url`     | Override base URL                       |

### Examples

```bash
# Generate compressed sitemap
python manage.py generate_sitemap -o sitemap.xml.gz --compress

# Generate only blog sitemap
python manage.py generate_sitemap --section blog -o blog-sitemap.xml

# Generate with custom base URL
python manage.py generate_sitemap --base-url https://www.example.com

# Generate URL list (for debugging)
python manage.py generate_sitemap --format txt
```

### Paginated Output

For large sitemaps:

```bash
# Generate index + section files
python manage.py generate_sitemap --output-dir ./sitemaps/ --limit 10000
```

This creates:

```
sitemaps/
├── sitemap.xml          # Index file
├── sitemap-blog-1.xml   # Blog page 1
├── sitemap-blog-2.xml   # Blog page 2
└── sitemap-static.xml   # Static pages
```

## validate_sitemap

Validate sitemap XML structure, URL accessibility, and compliance.

### Basic Usage

```bash
# Validate from URL
python manage.py validate_sitemap https://example.com/sitemap.xml

# Validate from file
python manage.py validate_sitemap ./sitemap.xml

# Validate all configured sitemaps
python manage.py validate_sitemap --all
```

### Options

| Option            | Description                          |
| ----------------- | ------------------------------------ |
| `--all`           | Validate all configured sitemaps     |
| `--strict`        | Strict validation (fail on warnings) |
| `--verbose`, `-v` | Show detailed output                 |
| `--check-urls`    | Verify URLs are accessible           |
| `--timeout`       | URL check timeout in seconds         |

### Validation Checks

The validator checks:

- **XML Structure** — Valid XML syntax
- **Schema Compliance** — Follows sitemap protocol
- **URL Format** — Valid, absolute URLs
- **URL Length** — Under 2,048 characters
- **URL Count** — Max 50,000 per sitemap
- **File Size** — Under 50MB uncompressed
- **Lastmod Format** — ISO 8601 dates
- **Priority Values** — Between 0.0 and 1.0
- **Changefreq Values** — Valid frequency strings

### Examples

```bash
# Verbose validation
python manage.py validate_sitemap --all -v

# Strict mode (warnings become errors)
python manage.py validate_sitemap sitemap.xml --strict

# Check that URLs return 200
python manage.py validate_sitemap sitemap.xml --check-urls --timeout 5
```

### Output

```
Validating: https://example.com/sitemap.xml
✓ Valid XML structure
✓ Valid sitemap schema
✓ 1,234 URLs found
✓ All URLs valid format
⚠ 3 URLs exceed recommended length
✓ All dates valid ISO 8601

Sitemap is valid!
```

## submit_sitemap

Submit sitemap to search engine ping endpoints.

### Basic Usage

```bash
# Submit configured sitemap
python manage.py submit_sitemap

# Submit specific URL
python manage.py submit_sitemap https://example.com/sitemap.xml
```

### Options

| Option       | Description                  |
| ------------ | ---------------------------- |
| `--google`   | Submit to Google only        |
| `--bing`     | Submit to Bing only          |
| `--endpoint` | Custom endpoint URL          |
| `--timeout`  | Request timeout in seconds   |
| `--dry-run`  | Show what would be submitted |

### Configuration

Configure default sitemap URL in settings:

```python
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

### Examples

```bash
# Submit to all configured endpoints
python manage.py submit_sitemap

# Submit to Google only
python manage.py submit_sitemap --google

# Submit to custom endpoint
python manage.py submit_sitemap --endpoint "https://search.example.com/ping?url={url}"

# Dry run (show what would happen)
python manage.py submit_sitemap --dry-run
```

### Output

```
Submitting sitemap: https://example.com/sitemap.xml

Endpoints:
  Google: https://www.google.com/ping?sitemap=...
  ✓ HTTP 200 OK

  Bing: https://www.bing.com/ping?sitemap=...
  ✓ HTTP 200 OK

Sitemap submitted successfully!
```

## clear_sitemap_cache

Clear cached sitemap data.

### Basic Usage

```bash
# Clear all sitemap cache
python manage.py clear_sitemap_cache

# Clear specific section
python manage.py clear_sitemap_cache --section blog
```

### Options

| Option      | Description                         |
| ----------- | ----------------------------------- |
| `--section` | Clear only specific sitemap section |
| `--dry-run` | Show what would be cleared          |

### Examples

```bash
# Clear all cache
python manage.py clear_sitemap_cache

# Clear only blog sitemap cache
python manage.py clear_sitemap_cache --section blog

# Preview what would be cleared
python manage.py clear_sitemap_cache --dry-run
```

### Output

```
Clearing sitemap cache...
  Cleared: swing_sitemap:blog
  Cleared: swing_sitemap:static
  Cleared: swing_sitemap:products

3 cache entries cleared.
```

## Celery Tasks

For async/scheduled operations, use Celery tasks instead of management commands.

### Submit Sitemap Task

```python
from swing.sitemap.tasks import submit_sitemap_task

# Submit immediately
submit_sitemap_task.delay()

# Submit specific URL
submit_sitemap_task.delay("https://example.com/sitemap.xml")
```

### Periodic Submission

```python
# celery.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    "submit-sitemap-daily": {
        "task": "swing.sitemap.tasks.submit_sitemap_periodic",
        "schedule": crontab(hour=6, minute=0),
    },
}
```

### Cache Invalidation Task

```python
from swing.sitemap.tasks import invalidate_sitemap_cache

# Clear all cache
invalidate_sitemap_cache.delay()

# Clear specific key
invalidate_sitemap_cache.delay("blog")
```

## Cron Examples

### Daily Sitemap Generation

```bash
# crontab
0 5 * * * cd /app && python manage.py generate_sitemap -o /var/www/sitemap.xml
```

### Weekly Submission

```bash
# crontab
0 6 * * 0 cd /app && python manage.py submit_sitemap
```

### Hourly Validation (Production)

```bash
# crontab
0 * * * * cd /app && python manage.py validate_sitemap --all >> /var/log/sitemap-validation.log 2>&1
```

## Exit Codes

| Code | Meaning                   |
| ---- | ------------------------- |
| 0    | Success                   |
| 1    | Validation failed / Error |
| 2    | Invalid arguments         |

Use exit codes in CI/CD pipelines:

```yaml
# GitHub Actions
- name: Validate sitemap
  run: python manage.py validate_sitemap --all --strict
```
