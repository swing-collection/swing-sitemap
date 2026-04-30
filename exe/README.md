# Demo Project for `swing-sitemap`

Self-contained Django project for testing and showcasing the
`swing-sitemap` reusable app in isolation.

## Setup

```bash
cd swing-sitemap
poetry install
```

## Usage

```bash
cd exe
python manage.py migrate
python manage.py createsuperuser    # optional
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. The Django admin is at
`/admin/`.

## Project Structure

```
exe/
├── demo/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── static/
└── README.md
```
