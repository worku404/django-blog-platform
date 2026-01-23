# Installation

This guide will walk you through setting up the Django Blog Project on your local machine.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (usually comes with Python)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **PostgreSQL** (optional but recommended) - [Download PostgreSQL](https://www.postgresql.org/download/)

You can verify installations:

```bash
python --version  # or python3 --version
pip --version     # or pip3 --version
git --version
psql --version    # if using PostgreSQL
```

---

## Step 1: Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/worku404/django-blog-project.git
cd django-blog-project
```

Navigate to the main project directory:

```bash
cd gold_blog
```

---

## Step 2: Create a Virtual Environment

Creating a virtual environment isolates your project dependencies:

### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt when the virtual environment is active.

---

## Step 3: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- Django 5.2
- psycopg 3.x (PostgreSQL adapter)
- python-decouple (configuration management)
- django-taggit (tagging system)
- Markdown (markdown support)
- sqlparse (SQL formatting)

---

## Step 4: Configure Environment Variables

Create a `.env` file in the `gold_blog` directory to store sensitive configuration:

```bash
touch .env  # On macOS/Linux
# On Windows, create the file manually or use: type nul > .env
```

Add the following variables to your `.env` file:

```env
# Database Configuration
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Email Configuration (for post sharing feature)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### Environment Variable Notes:

- **Database**: If using SQLite instead of PostgreSQL, you can skip the DB_* variables (see Configuration guide)
- **Email**: For Gmail, you'll need to create an [App Password](https://support.google.com/accounts/answer/185833)
- **Development**: For local testing, you can use fake email credentials (email features won't work but the app will run)

---

## Step 5: Set Up the Database

### Option A: PostgreSQL (Recommended)

1. **Create a PostgreSQL database:**

```bash
# Access PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE your_database_name;

# Create user (optional)
CREATE USER your_database_user WITH PASSWORD 'your_database_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_database_user;

# Exit
\q
```

2. **Verify your `.env` file matches these credentials**

3. **Enable trigram extension** (for search functionality):

```bash
psql -U postgres -d your_database_name

CREATE EXTENSION pg_trgm;

\q
```

### Option B: SQLite (Simple Alternative)

If you prefer to use SQLite for development:

1. **Edit `foodie/settings.py`** and comment out the PostgreSQL configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

2. **Note**: Full-text search features will be limited with SQLite

---

## Step 6: Run Database Migrations

Apply database migrations to create all necessary tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

You should see output showing the creation of tables for:
- Django auth and admin
- Blog posts
- Comments
- Tags (taggit)

---

## Step 7: Create a Superuser

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email address
- Password (enter twice for confirmation)

**Remember these credentials** - you'll need them to log into the admin panel.

---

## Step 8: Collect Static Files (Optional)

For production-like setups, collect static files:

```bash
python manage.py collectstatic
```

For local development, this step is optional as Django can serve static files directly.

---

## Step 9: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You should see output like:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## Step 10: Verify Installation

### Access the Blog

Open your web browser and navigate to:

- **Homepage**: http://127.0.0.1:8000/
- **Blog Posts**: http://127.0.0.1:8000/post/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### Test the Admin Panel

1. Go to http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. You should see the admin dashboard with Posts and Comments

---

## Troubleshooting

### Common Issues

#### Port Already in Use

If port 8000 is already in use:

```bash
python manage.py runserver 8080
```

#### Database Connection Error

- Verify PostgreSQL is running: `pg_isready`
- Check your `.env` file credentials
- Ensure the database exists
- Try using SQLite as a fallback

#### Module Not Found Error

```bash
pip install -r requirements.txt --upgrade
```

#### Static Files Not Loading

Make sure you have `{% load static %}` in your templates and check the `STATIC_URL` setting.

#### Email Errors

Email features will fail without proper SMTP configuration. For local development, you can:
- Use Django's console email backend (emails printed to console)
- Skip email testing
- Set up a Gmail App Password

---

## Optional: Load Sample Data

If the repository includes sample data:

```bash
python manage.py loaddata mysite_data.json
```

This will populate your database with sample posts and comments.

---

## Next Steps

Now that you have the project installed:

1. Read the [Configuration](configuration.md) guide for detailed settings
2. Learn how to [Run Locally](running-locally.md) for development
3. Explore [Usage](usage.md) to create your first blog post
4. Check out [Admin Usage](admin-usage.md) for content management

---

## Updating the Installation

To update your installation after pulling new changes:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
python manage.py migrate
python manage.py collectstatic --noinput
```

---

[← Back to Documentation Index](README.md)
