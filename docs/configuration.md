# Configuration

This guide covers all configuration options for the Django Blog Project, including environment variables, Django settings, and customization options.

## Environment Variables

Environment variables are managed using `python-decouple` and stored in a `.env` file.

### Creating the .env File

Create a `.env` file in the `gold_blog/` directory:

```bash
cd gold_blog
touch .env
```

### Required Environment Variables

#### Database Configuration

```bash
# PostgreSQL Database Settings
DB_NAME=django_blog_db
DB_USER=blog_user
DB_PASSWORD=your_secure_password_here
DB_HOST=127.0.0.1
DB_PORT=5432
```

**Parameters:**
- `DB_NAME`: Database name (must exist in PostgreSQL)
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: User's password
- `DB_HOST`: Database host (usually `127.0.0.1` for local)
- `DB_PORT`: PostgreSQL port (default: `5432`)

#### Email Configuration

```bash
# Email Server Settings
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate an App Password:
   - Go to Google Account → Security
   - Select "2-Step Verification"
   - Select "App passwords"
   - Generate password for "Mail"
3. Use the generated 16-character password as `EMAIL_HOST_PASSWORD`

**For Other Providers:**
Modify `foodie/settings.py`:
```python
EMAIL_HOST = 'smtp.yourprovider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### Optional Environment Variables

```bash
# Django Settings (override defaults)
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Production Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Environment Variable Loading

The project uses `python-decouple` to load environment variables:

```python
from decouple import config

# Usage in settings.py
DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER", default="postgres")
DEBUG = config("DEBUG", default=False, cast=bool)
```

**Benefits:**
- Secure: Keeps secrets out of version control
- Flexible: Different configs for dev/staging/prod
- Type Casting: Automatic conversion to bool, int, etc.

## Django Settings

### settings.py Location

```
gold_blog/foodie/settings.py
```

### Database Settings

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': config("DB_HOST", default="127.0.0.1"),
        'PORT': config("DB_PORT", default="5432"),
    }
}
```

**PostgreSQL Required:**
The project requires PostgreSQL for:
- Full-text search with trigram similarity
- Better performance for complex queries
- Production-ready reliability

### Email Settings

```python
# SMTP Configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
```

**Email Backends:**

**Development (Console):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Prints emails to console instead of sending.

**Production (SMTP):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

### Security Settings

#### Secret Key

```python
SECRET_KEY = config('SECRET_KEY', default='django-insecure-h6qb&dp299+dgh^z9f5w_m8u#$wz567(*c7m%!0jpyg-2l7@l@')
```

**Generate a New Secret Key:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

**⚠️ Security Warning:** Always use a unique, randomly generated secret key in production!

#### Debug Mode

```python
DEBUG = True  # Development only!
```

**Production:**
```python
DEBUG = False
```

When `DEBUG = False`:
- Error pages show generic messages
- Static files must be served by web server
- `ALLOWED_HOSTS` must be configured

#### Allowed Hosts

```python
ALLOWED_HOSTS = []  # Development

# Production
ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'your-server-ip',
]
```

### Installed Applications

```python
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    
    # Third-party apps
    'taggit',  # django-taggit for tags
    
    # Local apps
    'blog.apps.BlogConfig',
]
```

**Adding New Apps:**
1. Install via pip
2. Add to `INSTALLED_APPS`
3. Run migrations if needed

### Middleware Configuration

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### Template Settings

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Template Loading:**
- `APP_DIRS = True`: Looks for templates in each app's `templates/` directory
- Order matters: First match wins

### Static Files

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

**Development:**
Django serves static files automatically when `DEBUG = True`.

**Production:**
```bash
python manage.py collectstatic
```
Collects all static files to `STATIC_ROOT`.

### Media Files

For user uploads (if added):

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Internationalization

```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
```

**Change Time Zone:**
```python
TIME_ZONE = 'America/New_York'  # Or your timezone
```

[List of timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

### Site Framework

```python
SITE_ID = 1
```

Required for `django.contrib.sites` (used by feeds and sitemaps).

## Application Configuration

### Blog App Settings

#### Pagination

**File:** `gold_blog/blog/views.py`

```python
def post_list(request, tag_slug=None):
    # ...
    paginator = Paginator(post_list, 4)  # Posts per page
```

**Change to 10 posts per page:**
```python
paginator = Paginator(post_list, 10)
```

#### Comment Display

**File:** `gold_blog/blog/views.py`

```python
def Post_detail(request, year, month, day, post):
    # ...
    comment_limit = int(request.GET.get("climit", 3))  # Default: 3
```

**Change default to 5:**
```python
comment_limit = int(request.GET.get("climit", 5))
```

#### Similar Posts Count

**File:** `gold_blog/blog/views.py`

```python
def Post_detail(request, year, month, day, post):
    # ...
    similar_posts = similar_posts.order_by(...)[:4]  # Top 4
```

**Change to 6:**
```python
similar_posts = similar_posts.order_by(...)[:6]
```

### Taggit Configuration

**Custom settings** (optional):

```python
# In settings.py
TAGGIT_CASE_INSENSITIVE = True  # Default
TAGGIT_TAGS_FROM_STRING = 'taggit.utils.parse_tags'
TAGGIT_STRING_FROM_TAGS = 'taggit.utils.edit_string_for_tags'
```

## Production Configuration

### Security Checklist

```python
# settings.py - Production

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = config('SECRET_KEY')  # From environment

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Database Optimization

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': config("DB_HOST"),
        'PORT': config("DB_PORT"),
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

### Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/path/to/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Static Files Serving

**Production with Whitenoise:**

```bash
pip install whitenoise
```

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## Performance Tuning

### Caching

**Redis Cache:**

```bash
pip install redis django-redis
```

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

**Cache Templates:**
```python
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]
```

### Database Connection Pooling

```python
DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes
```

## Development vs Production

### settings_dev.py (Development)

```python
from .settings import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Usage:**
```bash
python manage.py runserver --settings=foodie.settings_dev
```

### settings_prod.py (Production)

```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
# ... production-specific settings
```

## Environment-Specific Settings

### Using Environment Variable

```python
# settings.py
import os

ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

if ENVIRONMENT == 'production':
    DEBUG = False
    # Production settings
else:
    DEBUG = True
    # Development settings
```

### .env Example

**Development (.env.dev):**
```bash
DJANGO_ENV=development
DEBUG=True
DB_NAME=django_blog_dev
```

**Production (.env.prod):**
```bash
DJANGO_ENV=production
DEBUG=False
DB_NAME=django_blog_prod
```

## Customization Examples

### Custom Homepage

```python
# blog/views.py
def home(request):
    latest_posts = Post.published.all()[:5]
    return render(request, 'blog/post/home.html', {
        'latest_posts': latest_posts
    })
```

### Change Site Name

```python
# settings.py
SITE_NAME = "My Awesome Blog"
SITE_DESCRIPTION = "Thoughts on coding and technology"
```

Use in templates:
```django
{% load static %}
<title>{{ SITE_NAME }}</title>
```

### Custom URL Patterns

```python
# blog/urls.py
urlpatterns = [
    path('articles/', views.post_list, name='post_list'),  # Change from 'post/'
    # ...
]
```

## Next Steps

- **[Development Guide](development.md)** - Set up development environment
- **[Deployment Guide](deployment.md)** - Deploy to production
- **[Troubleshooting](troubleshooting.md)** - Solve configuration issues

---

[← Back to Documentation Index](index.md) | [Next: Development →](development.md)
