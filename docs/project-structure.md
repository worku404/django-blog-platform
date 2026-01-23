# Project Structure

This document explains the directory layout and file organization of the Django Blog Project.

---

## Repository Overview

```
django-blog-project/
├── docs/                    # Documentation (this directory)
├── gold_blog/              # Main Django project directory
│   ├── blog/               # Blog application
│   ├── foodie/             # Project configuration
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
├── LICENSE                 # MIT License
└── README.md              # Project overview
```

---

## Root Directory

### `docs/`
Documentation directory containing:
- **README.md** - Documentation index
- **overview.md** - Project introduction
- **features.md** - Feature documentation
- **architecture.md** - Technical architecture
- **installation.md** - Setup guide
- **configuration.md** - Settings reference
- **running-locally.md** - Development guide
- **project-structure.md** - This file
- **usage.md** - User guide
- **admin-usage.md** - Admin guide
- **customization.md** - Customization guide
- **deployment.md** - Deployment guide
- **contributing.md** - Contribution guidelines

### `LICENSE`
MIT License file - defines usage rights and restrictions.

### `README.md`
Main project README with quick start guide and overview.

---

## Django Project (`gold_blog/`)

The main Django project directory containing all application code.

### `manage.py`
Django's command-line utility for administrative tasks:

```bash
python manage.py runserver    # Start development server
python manage.py migrate       # Apply database migrations
python manage.py createsuperuser  # Create admin user
python manage.py shell         # Django Python shell
python manage.py collectstatic # Collect static files
```

### `requirements.txt`
Python package dependencies:

```
asgiref~=3.8          # ASGI server reference
Django~=5.2           # Web framework
sqlparse==0.5.0       # SQL parser
python-decouple==3.8  # Configuration management
django-taggit==5.0.1  # Tagging system
Markdown==3.6         # Markdown support
psycopg==3.1.18       # PostgreSQL adapter
```

### `mysite_data.json`
Optional fixture file containing sample blog data for testing.

---

## Blog Application (`gold_blog/blog/`)

The core blog application containing all blogging functionality.

```
blog/
├── migrations/             # Database migrations
├── static/                # Static files (CSS, images)
├── templates/             # HTML templates
├── templatetags/          # Custom template tags
├── __init__.py           # Python package marker
├── admin.py              # Admin interface configuration
├── apps.py               # App configuration
├── feeds.py              # RSS/Atom feed configuration
├── form.py               # Form definitions
├── models.py             # Data models
├── sitemaps.py           # Sitemap configuration
├── tests.py              # Unit tests
├── urls.py               # URL routing
└── views.py              # View logic
```

### Core Files

#### `models.py`
Defines database models:

```python
Post              # Blog post model
├── title         # Post title
├── slug          # URL-friendly identifier
├── author        # Foreign key to User
├── body          # Post content
├── publish       # Publication date
├── status        # Draft or Published
└── tags          # Tag manager

Comment           # Comment model
├── post          # Foreign key to Post
├── name          # Commenter name
├── email         # Commenter email
├── body          # Comment content
└── active        # Moderation status
```

#### `views.py`
Contains view functions:

- **post_list()** - Display list of posts with pagination
- **Post_detail()** - Show individual post with comments
- **post_share()** - Email sharing form
- **post_comment()** - Handle comment submission
- **post_search()** - Full-text search functionality
- **home()** - Homepage view
- **kiya_view()** - Custom page view

#### `urls.py`
URL routing patterns:

```python
/                     → home
/post/                → post_list
/post/<date>/<slug>/  → Post_detail
/tag/<slug>/          → post_list_by_tag
/<id>/share/          → post_share
/<id>/comment/        → post_comment
/search/              → post_search
/feed/                → RSS feed
```

#### `admin.py`
Admin interface customization:

- **PostAdmin** - Post management interface
- **CommentAdmin** - Comment moderation interface

#### `forms.py`
Form definitions:

- **EmailPostForm** - Email sharing form
- **CommentForm** - Comment submission form
- **SearchForm** - Search input form

#### `feeds.py`
RSS/Atom feed configuration for latest posts.

#### `sitemaps.py`
Sitemap generation for SEO.

---

## Static Files (`blog/static/blog/`)

Static assets organized by type:

```
static/blog/
├── css/                   # Stylesheets
│   ├── blog.css          # Base styles
│   ├── list.css          # Post list styles
│   ├── detail.css        # Post detail styles
│   ├── home.css          # Homepage styles
│   ├── footer.css        # Footer styles
│   └── kiya.css          # Custom page styles
└── image/                # Images
    ├── logo.jpg          # Site logo
    ├── profile.jpg       # Profile images
    ├── photo*.jpg        # Content images
    └── *.png             # Various images
```

### CSS Architecture

- **blog.css** - Base styles, typography, layout
- **list.css** - Post listing page styles
- **detail.css** - Post detail page styles
- **home.css** - Homepage specific styles
- **footer.css** - Footer component styles

Each page loads its specific CSS file plus the base `blog.css`.

---

## Templates (`blog/templates/blog/`)

Template hierarchy and organization:

```
templates/blog/
├── base.html             # Base template (parent)
└── post/                # Post-related templates
    ├── list.html        # Post listing page
    ├── detail.html      # Post detail page
    ├── home.html        # Homepage
    ├── search.html      # Search results
    ├── share.html       # Email sharing page
    ├── comment.html     # Comment confirmation
    ├── pagination.html  # Pagination component
    ├── latest_posts.html # Latest posts widget
    ├── kiya.html        # Custom page
    └── includes/        # Reusable components
        ├── comment_form.html  # Comment form
        ├── search_form.html   # Search form
        └── footer.html        # Footer component
```

### Template Inheritance

```
base.html
├── home.html
├── list.html
├── detail.html
├── search.html
├── share.html
└── comment.html
```

All templates extend `base.html` and override specific blocks.

### Template Blocks

Common blocks in `base.html`:
- **title** - Page title
- **content** - Main content area
- **extra_css** - Additional stylesheets
- **extra_js** - Additional JavaScript

---

## Template Tags (`blog/templatetags/`)

Custom template tags for reusable functionality:

```
templatetags/
├── __init__.py          # Makes it a Python package
└── blog_tags.py         # Custom template tags
```

Usage in templates:
```django
{% load blog_tags %}
{% show_latest_posts %}
```

---

## Database Migrations (`blog/migrations/`)

```
migrations/
├── __init__.py          # Package marker
├── 0001_initial.py      # Initial models
├── 0002_*.py            # Subsequent changes
└── ...
```

Migrations track database schema changes over time.

**Common Commands:**
```bash
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
python manage.py showmigrations  # Show status
```

---

## Project Configuration (`gold_blog/foodie/`)

Django project settings and configuration:

```
foodie/
├── __init__.py          # Package marker
├── settings.py          # Main settings file
├── urls.py              # Root URL configuration
├── wsgi.py              # WSGI application
└── asgi.py              # ASGI application
```

### `settings.py`
Main configuration file containing:
- Database settings
- Installed apps
- Middleware configuration
- Template settings
- Static files configuration
- Email settings
- Security settings
- Internationalization

### `urls.py`
Root URL configuration:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('sitemap.xml', ...),
]
```

### `wsgi.py` & `asgi.py`
Server entry points for deployment:
- **WSGI** - Traditional synchronous servers
- **ASGI** - Asynchronous servers (for future features)

---

## Configuration Files

### `.env` (Not in Repository)
Environment variables for sensitive data:

```env
DB_NAME=database_name
DB_USER=database_user
DB_PASSWORD=secret_password
EMAIL_HOST_USER=email@example.com
EMAIL_HOST_PASSWORD=email_password
DEFAULT_FROM_EMAIL=noreply@example.com
```

⚠️ **Never commit this file to Git!**

### `.gitignore`
Specifies files to ignore in version control:

```
*.pyc
__pycache__/
db.sqlite3
.env
venv/
staticfiles/
```

---

## File Naming Conventions

The project follows Django and Python naming conventions:

### Python Files
- **Snake case** - `models.py`, `blog_tags.py`
- **Descriptive names** - `post_list`, `get_queryset`

### Templates
- **Lowercase with hyphens** - Not applicable here, uses underscores
- **Nested in app directory** - `blog/templates/blog/post/list.html`

### Static Files
- **Lowercase with hyphens/underscores** - `blog.css`, `post-list.js`
- **Organized by type** - `css/`, `image/`, `js/`

### URL Patterns
- **Lowercase with hyphens** - `/post/`, `/tag/`, `/search/`
- **RESTful naming** - Resource-based patterns

---

## Adding New Features

### To Add a New Model:

1. Edit `blog/models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Register in `blog/admin.py`

### To Add a New Page:

1. Create view in `blog/views.py`
2. Add URL pattern in `blog/urls.py`
3. Create template in `blog/templates/blog/`
4. Add CSS in `blog/static/blog/css/`

### To Add a New App:

1. Run `python manage.py startapp newapp`
2. Add to `INSTALLED_APPS` in `settings.py`
3. Include URLs in `foodie/urls.py`

---

## Best Practices

### File Organization

✅ **Do:**
- Keep related files together
- Use meaningful names
- Follow Django conventions
- Organize by feature/app

❌ **Don't:**
- Mix business logic in templates
- Store secrets in code
- Duplicate code across files
- Create circular imports

### Directory Structure

✅ **Do:**
- Use app directories for app-specific code
- Keep global configs in project directory
- Separate static files by type
- Use includes for reusable templates

❌ **Don't:**
- Put all templates in one directory
- Mix static files together
- Store media with static files
- Create deep nested directories unnecessarily

---

## File Relationships

### Model → View → Template Flow

```
models.py (Post)
    ↓
views.py (post_list)
    ↓
urls.py (path mapping)
    ↓
templates/blog/post/list.html
    ↓
static/blog/css/list.css
```

### Request Flow

```
Browser Request
    ↓
urls.py (URL matching)
    ↓
views.py (Business logic)
    ↓
models.py (Data access)
    ↓
templates/ (Rendering)
    ↓
Browser Response
```

---

[← Back to Documentation Index](README.md)
