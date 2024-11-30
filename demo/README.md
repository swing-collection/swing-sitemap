# Demo Project for `swing_hello`

This is a demo Django project designed to test and showcase the functionality of the `swing_hello` reusable Django app. The project provides a simple environment to experiment with the features of `swing_hello`.

---

## Installation

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/swing-collection/swing-hello.git
cd swing-hello
cd demo
```

### 2. Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If you are using poetry, install the dependencies using:

```bash
poetry install
```

## Usage

### 1. Apply Migrations

Run the following command to set up the database:

```bash
python manage.py migrate
```

### 2. Create a Superuser (Optional)

To access the Django admin interface, create a superuser:

```bash
python manage.py createsuperuser
```

### 3. Run the Development Server

Start the development server:

```bash
python manage.py runserver
```

Access the project in your web browser at `http://127.0.0.1:8000/`.

## Project Structure

```bash
demo/
├── demo/
│   ├── __init__.py        # Project package initialization
│   ├── settings.py        # Project settings
│   ├── urls.py            # URL configuration
│   ├── wsgi.py            # WSGI entry point
├── manage.py              # Django CLI entry point
├── db.sqlite3             # SQLite database file
├── README.md              # This README file
└── requirements.txt       # Python dependencies
```

## Features

- Django Admin: Access the admin interface at /admin/.
- Swing Hello App: Test the swing_hello reusable app at /hello/.
