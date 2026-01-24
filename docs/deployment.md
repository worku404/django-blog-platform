# Deployment Guide

This guide covers deploying the Django Blog Project to production environments.

## Pre-Deployment Checklist

Before deploying to production, ensure you have:

- [ ] Set `DEBUG = False` in settings
- [ ] Configured `ALLOWED_HOSTS`
- [ ] Set unique `SECRET_KEY` from environment variable
- [ ] Configured production database
- [ ] Set up email service
- [ ] Configured static file serving
- [ ] Set up HTTPS/SSL
- [ ] Configured logging
- [ ] Created backup strategy
- [ ] Tested thoroughly in staging environment

## Production Settings

### Environment Variables

Create `.env` file for production with:

```bash
# Django Settings
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=django_blog_prod
DB_USER=blog_user
DB_PASSWORD=secure_production_password
DB_HOST=your-db-host
DB_PORT=5432

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Security Settings

Add to `settings.py`:

```python
# Security for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

## Deployment Platforms

### Option 1: DigitalOcean Droplet

#### 1. Create Droplet

1. Create Ubuntu 22.04 LTS droplet
2. Choose appropriate size (minimum: 1GB RAM)
3. Add SSH key
4. Create droplet

#### 2. Initial Server Setup

```bash
# SSH into server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Create deploy user
adduser deploy
usermod -aG sudo deploy

# Switch to deploy user
su - deploy
```

#### 3. Install Dependencies

```bash
# Install Python and PostgreSQL
sudo apt install python3-pip python3-dev python3-venv
sudo apt install postgresql postgresql-contrib
sudo apt install nginx
sudo apt install supervisor
```

#### 4. Set Up PostgreSQL

```bash
sudo -u postgres psql

# In PostgreSQL shell
CREATE DATABASE django_blog_prod;
CREATE USER blog_user WITH PASSWORD 'secure_password';
ALTER ROLE blog_user SET client_encoding TO 'utf8';
ALTER ROLE blog_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE blog_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django_blog_prod TO blog_user;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
\q
```

#### 5. Deploy Application

```bash
# Clone repository
cd /home/deploy
git clone https://github.com/worku404/django-blog-project.git
cd django-blog-project/gold_blog

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
# Add production environment variables

# Run migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

#### 6. Configure Gunicorn

Create `/home/deploy/django-blog-project/gold_blog/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

Create supervisor config `/etc/supervisor/conf.d/django-blog.conf`:

```ini
[program:django-blog]
command=/home/deploy/django-blog-project/gold_blog/venv/bin/gunicorn foodie.wsgi:application -c /home/deploy/django-blog-project/gold_blog/gunicorn_config.py
directory=/home/deploy/django-blog-project/gold_blog
user=deploy
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/django-blog/gunicorn.log
stderr_logfile=/var/log/django-blog/gunicorn-error.log
```

```bash
# Create log directory
sudo mkdir -p /var/log/django-blog
sudo chown deploy:deploy /var/log/django-blog

# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start django-blog
```

#### 7. Configure Nginx

Create `/etc/nginx/sites-available/django-blog`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/deploy/django-blog-project/gold_blog/staticfiles/;
    }
    
    location /media/ {
        alias /home/deploy/django-blog-project/gold_blog/media/;
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

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/django-blog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 8. Set Up SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow prompts and select redirect option.

---

### Option 2: Heroku

#### 1. Prepare Application

Install Heroku CLI and create `Procfile`:

```
web: gunicorn foodie.wsgi --log-file -
```

Create `runtime.txt`:

```
python-3.11.0
```

Update `requirements.txt`:

```bash
pip install gunicorn dj-database-url whitenoise
pip freeze > requirements.txt
```

#### 2. Update Settings

```python
# settings.py
import dj_database_url

# Database
DATABASES['default'] = dj_database_url.config(
    default=config('DATABASE_URL'),
    conn_max_age=600
)

# Static files with whitenoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### 3. Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-blog-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set EMAIL_HOST_USER="your-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="your-app-password"
heroku config:set DEFAULT_FROM_EMAIL="noreply@yourdomain.com"

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser

# Open application
heroku open
```

---

### Option 3: AWS EC2

Similar to DigitalOcean but:

1. Launch EC2 instance (Ubuntu)
2. Configure security groups (ports 80, 443, 22)
3. Set up Elastic IP
4. Follow DigitalOcean steps above

---

### Option 4: Railway

#### 1. Prepare Application

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && gunicorn foodie.wsgi",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 2. Deploy

1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Add PostgreSQL database
4. Set environment variables
5. Deploy

---

## Database Migrations

### Running Migrations in Production

```bash
# Backup database first!
pg_dump django_blog_prod > backup_$(date +%Y%m%d).sql

# Run migrations
python manage.py migrate

# If issues occur, restore backup
psql django_blog_prod < backup_20260123.sql
```

### Zero-Downtime Migrations

1. Make migrations backward compatible
2. Deploy new code
3. Run migrations
4. Remove old code in next deployment

---

## Static Files

### Collecting Static Files

```bash
python manage.py collectstatic --noinput
```

### Using CDN (Optional)

Configure AWS S3 for static files:

```bash
pip install django-storages boto3
```

```python
# settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
```

---

## Monitoring and Logging

### Set Up Logging

```python
# settings.py
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
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django-blog/django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
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

### Monitor with Sentry

```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

---

## Backup Strategy

### Database Backups

```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/home/deploy/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump django_blog_prod > $BACKUP_DIR/backup_$DATE.sql
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

Add to crontab:
```bash
0 2 * * * /home/deploy/backup.sh
```

### Media Files Backup

```bash
rsync -av /home/deploy/django-blog-project/gold_blog/media/ backup-server:/backups/media/
```

---

## Performance Optimization

### Enable Caching

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

# Cache templates
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]
```

### Database Optimization

```python
# settings.py
DATABASES['default']['CONN_MAX_AGE'] = 600

# In views, use select_related and prefetch_related
Post.objects.select_related('author').prefetch_related('tags')
```

---

## Updating Production

### Update Workflow

```bash
# On server
cd /home/deploy/django-blog-project
source gold_blog/venv/bin/activate

# Pull changes
git pull origin main

# Install new dependencies
pip install -r gold_blog/requirements.txt

# Collect static files
cd gold_blog
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Restart application
sudo supervisorctl restart django-blog
```

---

## Troubleshooting

### Application Won't Start

Check logs:
```bash
sudo tail -f /var/log/django-blog/gunicorn.log
sudo tail -f /var/log/nginx/error.log
```

### 502 Bad Gateway

- Check if Gunicorn is running: `sudo supervisorctl status`
- Restart Gunicorn: `sudo supervisorctl restart django-blog`

### Static Files Not Loading

- Verify `STATIC_ROOT` and `STATIC_URL`
- Run `collectstatic` again
- Check Nginx configuration

---

## Next Steps

- **[Troubleshooting Guide](troubleshooting.md)** - Common production issues
- **[Configuration Guide](configuration.md)** - Advanced configuration
- **[Development Guide](development.md)** - Local development

---

[← Back to Documentation Index](index.md)
