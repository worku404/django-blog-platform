# Installation Guide

This guide will walk you through setting up the Django Blog Project on your local development environment.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** ([Download Python](https://www.python.org/downloads/))
- **PostgreSQL 12+** ([Download PostgreSQL](https://www.postgresql.org/download/))
- **Git** ([Download Git](https://git-scm.com/downloads))
- **pip** (usually comes with Python)
- **virtualenv** or **venv** (recommended for isolation)

## Step 1: Clone the Repository

```bash
git clone https://github.com/worku404/django-blog-project.git
cd django-blog-project
```

## Step 2: Set Up Virtual Environment

Creating a virtual environment helps isolate project dependencies from your system Python installation.

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

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

## Step 3: Install Dependencies

With your virtual environment activated, install the required Python packages:

```bash
cd gold_blog
pip install -r requirements.txt
```

### Required Packages

The `requirements.txt` includes:
- `Django~=5.2` - Web framework
- `psycopg==3.1.18` - PostgreSQL adapter
- `django-taggit==5.0.1` - Tagging functionality
- `Markdown==3.6` - Markdown support
- `python-decouple==3.8` - Environment variable management
- `asgiref~=3.8` - ASGI support
- `sqlparse==0.5.0` - SQL parsing utilities

## Step 4: Set Up PostgreSQL Database

### Create Database

1. Open PostgreSQL command line or use a GUI tool like pgAdmin

2. Create a new database:
```sql
CREATE DATABASE django_blog_db;
```

3. Create a database user (optional but recommended):
```sql
CREATE USER blog_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE django_blog_db TO blog_user;
```

4. Enable the PostgreSQL trigram extension (required for search):
```sql
\c django_blog_db
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

## Step 5: Configure Environment Variables

Create a `.env` file in the `gold_blog/` directory with your configuration:

```bash
# Database Configuration
DB_NAME=django_blog_db
DB_USER=blog_user
DB_PASSWORD=your_secure_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Email Configuration (for sharing posts via email)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### Email Configuration Notes

- For Gmail, you need to use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password
- Ensure "Less secure app access" is enabled or use OAuth2
- For development, you can skip email configuration if you don't need the sharing feature

**Security Warning:** Never commit the `.env` file to version control. It's already included in `.gitignore`.

## Step 6: Apply Database Migrations

Run Django migrations to create the necessary database tables:

```bash
python manage.py migrate
```

This command will:
- Create all necessary tables for Django apps
- Set up the blog models (Post, Comment)
- Configure authentication and session tables
- Apply the trigram extension migration

## Step 7: Create a Superuser

Create an admin account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email address
- Password (enter twice for confirmation)

## Step 8: Load Sample Data (Optional)

If you want to start with sample data, you can load the provided fixture:

```bash
python manage.py loaddata mysite_data.json
```

This will populate your database with sample blog posts.

## Step 9: Collect Static Files (Production Only)

For development, Django serves static files automatically. For production:

```bash
python manage.py collectstatic
```

## Step 10: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Step 11: Verify Installation

Open your browser and visit:

- **Home Page:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Blog Posts:** [http://127.0.0.1:8000/post/](http://127.0.0.1:8000/post/)
- **Admin Interface:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Login to the admin interface with the superuser credentials you created.

## Common Installation Issues

### Issue: `psycopg` installation fails

**Solution:** Install PostgreSQL development headers:
- Ubuntu/Debian: `sudo apt-get install libpq-dev python3-dev`
- macOS: `brew install postgresql`
- Windows: Ensure PostgreSQL is in your PATH

### Issue: Database connection error

**Solution:** 
- Verify PostgreSQL is running
- Check your `.env` file has correct credentials
- Ensure the database exists: `psql -l | grep django_blog_db`

### Issue: Migration errors

**Solution:**
- Drop and recreate the database if starting fresh
- Ensure `pg_trgm` extension is installed
- Check migration files in `blog/migrations/`

## Next Steps

- **[Quick Start Guide](getting-started.md)** - Learn basic usage
- **[Configuration Guide](configuration.md)** - Customize settings
- **[Development Guide](development.md)** - Start developing

## Upgrading

To upgrade to a newer version:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
python manage.py migrate
python manage.py collectstatic --noinput
```

---

[← Back to Documentation Index](index.md)
