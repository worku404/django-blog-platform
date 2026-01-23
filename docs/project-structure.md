# Project Structure

This document provides a comprehensive overview of the Django Blog Project's architecture, directory organization, and key components.

## Directory Tree

```
django-blog-project/
├── gold_blog/                    # Main Django project directory
│   ├── blog/                     # Blog application
│   │   ├── migrations/           # Database migration files
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_post_author.py
│   │   │   ├── 0003_alter_post_id_alter_post_slug.py
│   │   │   ├── 0004_comment.py
│   │   │   ├── 0005_alter_post_id.py
│   │   │   ├── 0006_post_tags.py
│   │   │   ├── 0007_trigram_ext.py
│   │   │   └── __init__.py
│   │   ├── static/               # Static files (CSS, images, JS)
│   │   │   └── blog/
│   │   │       ├── css/          # Stylesheets
│   │   │       └── image/        # Images
│   │   ├── templates/            # HTML templates
│   │   │   └── blog/
│   │   │       └── post/         # Post-related templates
│   │   │           └── includes/ # Reusable template fragments
│   │   ├── templatetags/         # Custom template tags
│   │   │   ├── __init__.py
│   │   │   └── blog_tags.py
│   │   ├── __init__.py
│   │   ├── admin.py              # Admin interface configuration
│   │   ├── apps.py               # App configuration
│   │   ├── feeds.py              # RSS feed definitions
│   │   ├── form.py               # Form definitions
│   │   ├── models.py             # Data models
│   │   ├── sitemaps.py           # Sitemap configuration
│   │   ├── tests.py              # Test cases
│   │   ├── urls.py               # URL routing
│   │   └── views.py              # View functions
│   ├── foodie/                   # Project configuration
│   │   ├── __init__.py
│   │   ├── asgi.py               # ASGI configuration
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # Root URL configuration
│   │   └── wsgi.py               # WSGI configuration
│   ├── manage.py                 # Django management script
│   ├── mysite_data.json          # Sample data fixture
│   └── requirements.txt          # Python dependencies
├── docs/                         # Documentation
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
└── README.md                     # Project overview
```

## Core Components

### 1. Django Project (`foodie/`)

The main project configuration directory, named "foodie" (Django's default project structure).

#### `settings.py`
Central configuration file containing:
- Database settings (PostgreSQL configuration)
- Installed applications
- Middleware configuration
- Template settings
- Static files configuration
- Email server settings
- Security settings

**Key Settings:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',     # Blog application
    'taggit',                    # Tagging functionality
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # Connection details from .env
    }
}
```

#### `urls.py`
Root URL configuration that includes:
- Admin interface URLs
- Blog app URLs
- Sitemap URLs

#### `wsgi.py` & `asgi.py`
Entry points for WSGI/ASGI-compatible web servers in production.

### 2. Blog Application (`blog/`)

The main application containing all blog functionality.

#### `models.py`
Defines the data structure with two main models:

**Post Model:**
- `title`: CharField - Post title
- `slug`: SlugField - URL-friendly identifier
- `author`: ForeignKey - Links to Django User model
- `body`: TextField - Post content
- `publish`: DateTimeField - Publication date/time
- `created`: DateTimeField - Creation timestamp
- `updated`: DateTimeField - Last update timestamp
- `status`: CharField - Draft or Published
- `tags`: TaggableManager - Tag associations

**Post Features:**
- Custom manager `PublishedManager` for published posts only
- `get_absolute_url()` method for canonical URLs
- Meta options for ordering and indexing

**Comment Model:**
- `post`: ForeignKey - Associated blog post
- `name`: CharField - Commenter's name
- `email`: EmailField - Commenter's email
- `body`: TextField - Comment content
- `created`: DateTimeField - Creation timestamp
- `updated`: DateTimeField - Update timestamp
- `active`: BooleanField - Moderation flag

#### `views.py`
Contains all view functions:

| View | Purpose | URL Pattern |
|------|---------|-------------|
| `home` | Homepage | `/` |
| `post_list` | List all posts with pagination | `/post/` |
| `post_list` (with tag) | Filter posts by tag | `/tag/<slug>/` |
| `Post_detail` | Display single post with comments | `/post/YYYY/MM/DD/<slug>/` |
| `post_share` | Share post via email | `/<id>/share/` |
| `post_comment` | Handle comment submission | `/<id>/comment/` |
| `post_search` | Search posts | `/search/` |

**View Patterns:**
- Function-based views (FBVs) used throughout
- Uses `get_object_or_404` for safe object retrieval
- Implements pagination with Django's `Paginator`
- Uses PostgreSQL full-text search with trigram similarity

#### `urls.py`
URL routing for the blog app using Django's `path()`:
- Named URL patterns for reverse URL resolution
- RESTful URL structure with date-based permalinks
- Clean, SEO-friendly URLs

#### `admin.py`
Customizes the Django admin interface:

**PostAdmin:**
- List display with title, slug, author, publish date, status
- Filtering by status, created, publish dates
- Auto-populated slug field
- Search functionality for title and body
- Date hierarchy navigation

**CommentAdmin:**
- List display with name, email, post, created, active status
- Filtering by active status and dates
- Search by name, email, body

#### `form.py`
Defines forms for user interactions:

- `EmailPostForm`: Share posts via email
- `CommentForm`: Submit comments (ModelForm)
- `SearchForm`: Search functionality

#### `feeds.py`
RSS feed implementation for blog posts using Django's syndication framework.

#### `sitemaps.py`
XML sitemap generation for SEO purposes.

#### `templatetags/blog_tags.py`
Custom template tags and filters for reusable template logic.

### 3. Templates (`blog/templates/blog/`)

Django templates using the template engine:

```
blog/templates/blog/
├── base.html                 # Base template (if exists)
└── post/
    ├── list.html             # Post listing page
    ├── detail.html           # Post detail page
    ├── share.html            # Email sharing form
    ├── comment.html          # Comment submission response
    ├── search.html           # Search results page
    └── includes/             # Reusable template fragments
```

**Template Structure:**
- Template inheritance for DRY code
- Template tags for dynamic content
- Context processors for global data
- Responsive HTML/CSS layout

### 4. Static Files (`blog/static/blog/`)

Static assets served by Django:

```
static/blog/
├── css/                      # Stylesheets
│   └── *.css
└── image/                    # Images
    └── *.jpg, *.png
```

## Data Flow Architecture

### Request-Response Cycle

```
1. User Request
   ↓
2. urls.py (URL Routing)
   ↓
3. views.py (Business Logic)
   ↓
4. models.py (Database Query)
   ↓
5. templates/ (Render HTML)
   ↓
6. Response to User
```

### Example: Viewing a Blog Post

```
GET /post/2026/01/23/my-first-post/
   ↓
blog/urls.py → matches pattern
   ↓
views.Post_detail() → retrieves post, comments, similar posts
   ↓
Post.objects.get() → queries database
   ↓
blog/post/detail.html → renders template
   ↓
HTML response with post content
```

## Database Schema

### Entity Relationship Diagram

```
┌─────────────┐
│    User     │ (Django built-in)
└──────┬──────┘
       │ 1
       │
       │ N
┌──────┴──────┐
│    Post     │
│             │
│  - title    │
│  - slug     │
│  - body     │
│  - status   │
│  - publish  │
└──────┬──────┘
       │ 1
       │
       │ N
┌──────┴──────┐         ┌────────────┐
│  Comment    │         │    Tag     │ (django-taggit)
│             │         └──────┬─────┘
│  - name     │                │
│  - email    │         Many-to-Many
│  - body     │                │
│  - active   │         ┌──────┴─────┐
└─────────────┘         │ TaggedItem │
                        └────────────┘
```

### Relationships

- **User ↔ Post**: One-to-Many (one user can have many posts)
- **Post ↔ Comment**: One-to-Many (one post can have many comments)
- **Post ↔ Tag**: Many-to-Many (posts can have multiple tags, tags can be on multiple posts)

## Application Settings

### Environment Variables

Required variables in `.env`:

```bash
# Database
DB_NAME=django_blog_db
DB_USER=blog_user
DB_PASSWORD=secure_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Email
EMAIL_HOST_USER=email@example.com
EMAIL_HOST_PASSWORD=app_password
DEFAULT_FROM_EMAIL=email@example.com
```

### Important Settings

- **DEBUG**: Set to `True` in development, `False` in production
- **SECRET_KEY**: Django secret key (should be unique and secret)
- **ALLOWED_HOSTS**: List of allowed hostnames
- **DATABASES**: PostgreSQL connection details
- **STATIC_URL**: URL prefix for static files
- **MEDIA_URL**: URL prefix for user-uploaded files

## Key Design Patterns

### 1. Model-View-Template (MVT)
Django's implementation of MVC:
- **Model**: Data layer (`models.py`)
- **View**: Business logic (`views.py`)
- **Template**: Presentation layer (`templates/`)

### 2. Custom Managers
`PublishedManager` for filtering published posts:
```python
Post.published.all()  # Only published posts
```

### 3. Slugs for URLs
SEO-friendly URLs using slugs:
```
/post/2026/01/23/my-first-post/
```

### 4. Date-based Permalinks
Prevents slug collisions and provides temporal context:
```
/post/YYYY/MM/DD/slug/
```

### 5. QuerySet Optimization
- Prefetching related objects
- Select related for foreign keys
- Annotation for aggregation

## Extension Points

Areas designed for easy customization:

1. **Custom Template Tags** - Add new tags in `templatetags/`
2. **Additional Models** - Extend with categories, likes, etc.
3. **New Views** - Add features like archives, author pages
4. **Form Customization** - Modify or add new forms
5. **Admin Customization** - Enhance admin interface
6. **Static Assets** - Update CSS/JS for different themes

## Dependencies

### Core Dependencies

- **Django 5.2**: Web framework
- **psycopg 3.1.18**: PostgreSQL adapter
- **django-taggit 5.0.1**: Tagging system
- **Markdown 3.6**: Markdown processing
- **python-decouple 3.8**: Environment variable management

### Why PostgreSQL?

PostgreSQL is used for:
- Full-text search capabilities
- Trigram similarity matching
- Better performance for complex queries
- Production-ready database engine

## Next Steps

- **[Features Documentation](features.md)** - Learn about all features
- **[API Reference](api-reference.md)** - Detailed API documentation
- **[Development Guide](development.md)** - Development best practices

---

[← Back to Documentation Index](index.md) | [Next: Features →](features.md)
