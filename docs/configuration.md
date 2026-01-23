# Configuration

This guide covers all configuration options and settings for the Django Blog Project.

---

## Configuration Files

### Main Settings File

The primary configuration is in `gold_blog/foodie/settings.py`. This follows Django's standard settings structure.

### Environment Variables

Sensitive data is stored in `gold_blog/.env` using python-decouple for security.

---

## Environment Variables

Create a `.env` file in the `gold_blog` directory with the following variables:

### Database Configuration

```env
# PostgreSQL settings
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

**Notes:**
- Required when using PostgreSQL
- Can be omitted if using SQLite (see Database Configuration below)
- Host is typically `127.0.0.1` for local development
- Default PostgreSQL port is `5432`

### Email Configuration

```env
# Email server settings
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password_here
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

**Notes:**
- Required for email sharing feature
- For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password
- `EMAIL_HOST_PASSWORD` should be the app-specific password
- For development, these can be dummy values if you don't need email functionality

---

## Database Configuration

### PostgreSQL (Recommended)

The default configuration uses PostgreSQL:

```python
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config('DB_NAME'),
        "USER": config('DB_USER'),
        "PASSWORD": config('DB_PASSWORD'),
        "HOST": config('DB_HOST', default="127.0.0.1"),
        "PORT": config('DB_PORT', default="5432"),
        "OPTIONS": {
            'pool': {
                'min_size': 2,
                'max_size': 4,
                'timeout': 10,
            }
        }
    }
}
```

**Features:**
- Connection pooling (2-4 connections)
- Full-text search support
- Trigram similarity for advanced search
- Better performance for production

**PostgreSQL Extensions Required:**
```sql
CREATE EXTENSION pg_trgm;  -- For trigram search
```

### SQLite (Development Alternative)

For simpler local development, switch to SQLite by modifying `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Notes:**
- No additional setup required
- Single file database
- Full-text search features limited
- Not recommended for production

---

## Email Configuration

### SMTP Settings

Current configuration in `settings.py`:

```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
```

### Using Gmail

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate an App Password:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Create a new app password for "Mail"
3. **Use the app password** in your `.env` file

### Using Other Email Providers

#### Mailgun:
```python
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

#### SendGrid:
```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your_sendgrid_api_key'
```

#### Outlook/Office 365:
```python
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### Console Email Backend (Development)

For development without email setup, use console backend:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Emails will print to the console instead of sending.

---

## Security Settings

### Secret Key

⚠️ **IMPORTANT**: Change the secret key for production!

Current (development only):
```python
SECRET_KEY = 'django-insecure-h6qb&dp299+dgh^z9f5w_m8u#$wz567(*c7m%!0jpyg-2l7@l@'
```

**For Production:**
1. Generate a new secret key:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

2. Add to `.env`:
```env
SECRET_KEY=your_new_secret_key_here
```

3. Update `settings.py`:
```python
SECRET_KEY = config('SECRET_KEY')
```

### Debug Mode

```python
DEBUG = True  # Development
DEBUG = False  # Production
```

⚠️ **Never run production with DEBUG = True!**

For production, add to `.env`:
```env
DEBUG=False
```

Then in `settings.py`:
```python
DEBUG = config('DEBUG', default=False, cast=bool)
```

### Allowed Hosts

Configure allowed hosts for production:

```python
# Development
ALLOWED_HOSTS = []

# Production
ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'your-server-ip',
]
```

---

## Static Files Configuration

### Development Settings

```python
STATIC_URL = '/static/'
```

Django serves static files automatically in development.

### Production Settings

Add to `settings.py`:

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

Then collect static files:
```bash
python manage.py collectstatic
```

---

## Installed Apps

Current apps in `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',        # Admin interface
    'django.contrib.auth',         # Authentication
    'django.contrib.contenttypes', # Content types framework
    'django.contrib.sessions',     # Session framework
    'django.contrib.messages',     # Messaging framework
    'django.contrib.sites',        # Sites framework
    'django.contrib.sitemaps',     # Sitemap generation
    'django.contrib.staticfiles',  # Static file management
    'django.contrib.postgres',     # PostgreSQL features
    'blog.apps.BlogConfig',        # Main blog app
    'taggit',                      # Tagging system
]
```

### Adding Custom Apps

To add new functionality:

1. Create the app:
```bash
python manage.py startapp myapp
```

2. Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... existing apps ...
    'myapp.apps.MyappConfig',
]
```

---

## Middleware Configuration

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

### Production Middleware

For production, consider adding:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    # ... rest of middleware ...
]

# WhiteNoise settings
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## Template Configuration

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Notes:**
- `APP_DIRS = True` enables per-app template directories
- Global templates can go in `gold_blog/templates/`
- App-specific templates in `blog/templates/`

---

## Sites Framework

```python
SITE_ID = 1
```

Required for:
- Sitemap generation
- RSS feeds
- Absolute URL generation

**Setup:**
```bash
python manage.py shell
```

```python
from django.contrib.sites.models import Site
site = Site.objects.get(id=1)
site.domain = 'yourdomain.com'
site.name = 'Your Blog Name'
site.save()
```

---

## Internationalization

```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
```

### Changing Timezone

To use your local timezone:

```python
TIME_ZONE = 'America/New_York'  # Example
# Or
TIME_ZONE = 'Europe/London'
TIME_ZONE = 'Asia/Tokyo'
```

See [list of timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

---

## Password Validation

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

These validators ensure:
- Passwords aren't too similar to user info
- Minimum length requirement
- Common passwords are rejected
- Purely numeric passwords are rejected

---

## Performance Settings

### Database Connection Pooling

Already configured in PostgreSQL settings:

```python
"OPTIONS": {
    'pool': {
        'min_size': 2,      # Minimum connections
        'max_size': 4,      # Maximum connections
        'timeout': 10,      # Connection timeout
    }
}
```

### Caching (Optional)

For production, add caching:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

Or use database caching:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
```

---

## Logging Configuration

Add logging for production monitoring:

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

---

## Configuration Checklist for Production

- [ ] Set `DEBUG = False`
- [ ] Generate and use a new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up proper database (PostgreSQL)
- [ ] Configure static files serving
- [ ] Set up email backend properly
- [ ] Enable HTTPS/SSL
- [ ] Configure logging
- [ ] Set up caching (optional but recommended)
- [ ] Review security middleware settings
- [ ] Set proper timezone
- [ ] Configure backup strategy

---

## Environment-Specific Settings

Consider using different settings files:

```
foodie/
├── settings/
│   ├── __init__.py
│   ├── base.py       # Common settings
│   ├── development.py
│   └── production.py
```

Then use:
```bash
export DJANGO_SETTINGS_MODULE=foodie.settings.production
```

---

[← Back to Documentation Index](README.md)
