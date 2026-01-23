# Deployment

This guide covers deploying the Django Blog Project to production environments.

---

## Pre-Deployment Checklist

Before deploying to production, ensure you've completed:

- [ ] Set `DEBUG = False` in settings
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Generate a new `SECRET_KEY` (don't use the default)
- [ ] Set up environment variables for sensitive data
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up proper email backend
- [ ] Configure static files serving
- [ ] Set up HTTPS/SSL certificate
- [ ] Review security settings
- [ ] Test all functionality locally
- [ ] Set up error logging
- [ ] Configure database backups
- [ ] Prepare a rollback plan

---

## Environment Configuration

### Production Settings

Create `foodie/settings_production.py`:

```python
from .settings import *

DEBUG = False

ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'your-server-ip',
]

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static and Media Files
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 600,
    }
}

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
    }
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}
```

### Environment Variables

Production `.env` file:

```env
# Security
SECRET_KEY=your_new_production_secret_key_here
DEBUG=False

# Database
DB_NAME=production_db_name
DB_USER=production_db_user
DB_PASSWORD=strong_db_password
DB_HOST=db.yourdomain.com
DB_PORT=5432

# Email
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=email_app_password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Cache
REDIS_URL=redis://127.0.0.1:6379/1

# Domain
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

---

## Deployment Platforms

### Option 1: Traditional VPS (Ubuntu/Debian)

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv postgresql nginx supervisor

# Install Redis (optional, for caching)
sudo apt install -y redis-server
```

#### 2. PostgreSQL Setup

```bash
# Access PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE blog_production;
CREATE USER blog_user WITH PASSWORD 'strong_password';
ALTER ROLE blog_user SET client_encoding TO 'utf8';
ALTER ROLE blog_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE blog_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE blog_production TO blog_user;

# Enable trigram extension
\c blog_production
CREATE EXTENSION pg_trgm;

# Exit
\q
```

#### 3. Application Deployment

```bash
# Create app directory
sudo mkdir -p /var/www/django-blog
cd /var/www/django-blog

# Clone repository
sudo git clone https://github.com/worku404/django-blog-project.git .

# Create virtual environment
sudo python3 -m venv venv
sudo chown -R www-data:www-data /var/www/django-blog

# Activate and install dependencies
source venv/bin/activate
pip install -r gold_blog/requirements.txt
pip install gunicorn  # Production server

# Create .env file
sudo nano gold_blog/.env
# Add production environment variables

# Collect static files
cd gold_blog
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

#### 4. Gunicorn Configuration

Create `/etc/supervisor/conf.d/django-blog.conf`:

```ini
[program:django-blog]
command=/var/www/django-blog/venv/bin/gunicorn foodie.wsgi:application --bind 127.0.0.1:8000 --workers 3
directory=/var/www/django-blog/gold_blog
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/django-blog/gunicorn.log
stderr_logfile=/var/log/django-blog/gunicorn-error.log
```

Start Gunicorn:

```bash
sudo mkdir -p /var/log/django-blog
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start django-blog
```

#### 5. Nginx Configuration

Create `/etc/nginx/sites-available/django-blog`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/django-blog/gold_blog/staticfiles/;
    }

    location /media/ {
        alias /var/www/django-blog/gold_blog/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/django-blog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (should be configured automatically)
sudo certbot renew --dry-run
```

---

### Option 2: Heroku Deployment

#### 1. Prepare for Heroku

Install additional packages:

```bash
pip install gunicorn whitenoise dj-database-url psycopg2-binary
pip freeze > requirements.txt
```

Create `Procfile` in project root:

```
web: cd gold_blog && gunicorn foodie.wsgi
```

Create `runtime.txt`:

```
python-3.11.0
```

#### 2. Update Settings for Heroku

Add to `settings.py`:

```python
import dj_database_url

# Heroku specific settings
if 'DYNO' in os.environ:  # Running on Heroku
    DEBUG = False
    ALLOWED_HOSTS = ['.herokuapp.com']
    
    # Database
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)
    
    # Static files with WhiteNoise
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
```

#### 3. Deploy to Heroku

```bash
# Install Heroku CLI
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-blog-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set EMAIL_HOST_USER='your-email@gmail.com'
heroku config:set EMAIL_HOST_PASSWORD='your-app-password'

# Deploy
git push heroku main

# Run migrations
heroku run python gold_blog/manage.py migrate

# Create superuser
heroku run python gold_blog/manage.py createsuperuser

# Open app
heroku open
```

---

### Option 3: DigitalOcean App Platform

#### 1. Prepare Application

Similar to Heroku, ensure you have:
- `requirements.txt`
- `Procfile` or use web service configuration
- Environment variables ready

#### 2. Deploy via DigitalOcean

1. Go to DigitalOcean App Platform
2. Connect your GitHub repository
3. Configure:
   - **Source Directory**: `gold_blog`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Run Command**: `gunicorn foodie.wsgi:application`
4. Add PostgreSQL database component
5. Set environment variables in dashboard
6. Deploy

---

### Option 4: AWS EC2

Similar to traditional VPS setup, but:

1. Launch EC2 instance (Ubuntu recommended)
2. Configure security groups (ports 80, 443, 22)
3. Follow VPS deployment steps above
4. Consider using:
   - **RDS** for PostgreSQL database
   - **S3** for static/media files
   - **CloudFront** for CDN
   - **ELB** for load balancing

---

## Static Files in Production

### Using WhiteNoise (Simple)

Install:

```bash
pip install whitenoise
```

Configure in `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add here
    # ... rest of middleware ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Using CDN (Advanced)

For high-traffic sites, use a CDN:

1. Upload static files to S3
2. Configure CloudFront distribution
3. Update `STATIC_URL` in settings:

```python
STATIC_URL = 'https://d1234567890.cloudfront.net/static/'
```

---

## Database Backups

### Automated PostgreSQL Backups

Create backup script `/usr/local/bin/backup-db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/django-blog"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="blog_production"
DB_USER="blog_user"

mkdir -p $BACKUP_DIR

pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

Make executable and add to cron:

```bash
sudo chmod +x /usr/local/bin/backup-db.sh
sudo crontab -e

# Add line (daily at 2 AM):
0 2 * * * /usr/local/bin/backup-db.sh
```

---

## Monitoring and Maintenance

### Health Check Endpoint

Add to `blog/views.py`:

```python
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({'status': 'healthy'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=500)
```

Add URL:

```python
path('health/', views.health_check, name='health_check'),
```

### Error Monitoring

Use Sentry for error tracking:

```bash
pip install sentry-sdk
```

Configure in `settings.py`:

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

---

## Performance Monitoring

### Using Django Debug Toolbar (Dev Only)

Already covered in development docs.

### Using New Relic (Production)

```bash
pip install newrelic
newrelic-admin generate-config YOUR_LICENSE_KEY newrelic.ini
```

Update Procfile:

```
web: newrelic-admin run-program gunicorn foodie.wsgi
```

---

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (Nginx, HAProxy)
- Run multiple Gunicorn instances
- Database read replicas
- Redis for caching and sessions

### Vertical Scaling

- Increase server resources
- Optimize database queries
- Enable caching
- Use CDN for static files

---

## Troubleshooting Production Issues

### Application Won't Start

Check:
- Gunicorn logs: `tail -f /var/log/django-blog/gunicorn.log`
- Nginx logs: `tail -f /var/log/nginx/error.log`
- Environment variables are set
- Database is accessible

### Static Files Not Loading

- Run `collectstatic` again
- Check Nginx configuration
- Verify file permissions
- Check `STATIC_ROOT` and `STATIC_URL`

### Database Connection Errors

- Verify database credentials
- Check PostgreSQL is running
- Test connection: `psql -U blog_user -d blog_production`
- Check firewall rules

---

## Security Best Practices

- [ ] Use HTTPS only
- [ ] Keep Django and dependencies updated
- [ ] Use strong passwords
- [ ] Regular security audits
- [ ] Monitor logs for suspicious activity
- [ ] Implement rate limiting
- [ ] Use security headers
- [ ] Regular backups
- [ ] Principle of least privilege

---

[← Back to Documentation Index](README.md)
