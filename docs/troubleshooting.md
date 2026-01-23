# Troubleshooting

This guide helps you diagnose and resolve common issues with the Django Blog Project.

## Installation Issues

### Issue: `psycopg` Installation Fails

**Symptoms:**
```
ERROR: Failed building wheel for psycopg
```

**Solutions:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install libpq-dev python3-dev build-essential
pip install psycopg
```

**macOS:**
```bash
brew install postgresql
pip install psycopg
```

**Windows:**
1. Download PostgreSQL installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Install PostgreSQL (includes development headers)
3. Add PostgreSQL bin directory to PATH
4. Restart terminal and try: `pip install psycopg`

---

### Issue: Virtual Environment Not Activating

**Symptoms:**
- Command not found
- Wrong Python version

**Solutions:**

**Linux/macOS:**
```bash
# Ensure you created venv
python3 -m venv venv

# Try different activation method
. venv/bin/activate

# Or use full path
source $(pwd)/venv/bin/activate
```

**Windows:**
```bash
# PowerShell
venv\Scripts\Activate.ps1

# CMD
venv\Scripts\activate.bat

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Issue: Permission Denied During Installation

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

**Don't use sudo with pip:**
```bash
# Wrong
sudo pip install -r requirements.txt

# Correct
pip install -r requirements.txt
```

**Ensure virtual environment is activated:**
```bash
which python  # Should show venv path
```

---

## Database Issues

### Issue: Cannot Connect to Database

**Symptoms:**
```
django.db.utils.OperationalError: could not connect to server
```

**Solutions:**

**Check PostgreSQL is running:**
```bash
# Linux
sudo systemctl status postgresql

# macOS
brew services list | grep postgresql

# Windows
# Check Services app for PostgreSQL service
```

**Start PostgreSQL if stopped:**
```bash
# Linux
sudo systemctl start postgresql

# macOS
brew services start postgresql

# Windows
net start postgresql-x64-14
```

**Verify credentials in .env:**
```bash
DB_NAME=django_blog_db
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

**Test connection:**
```bash
psql -U your_username -d django_blog_db -h 127.0.0.1
```

---

### Issue: Database Does Not Exist

**Symptoms:**
```
django.db.utils.OperationalError: database "django_blog_db" does not exist
```

**Solution:**

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE django_blog_db;

# Grant permissions
GRANT ALL PRIVILEGES ON DATABASE django_blog_db TO your_username;

# Exit
\q
```

---

### Issue: pg_trgm Extension Not Found

**Symptoms:**
```
django.db.utils.ProgrammingError: type "gtrgm" does not exist
```

**Solution:**

```bash
# Connect to your database
psql -U your_username -d django_blog_db

# Create extension
CREATE EXTENSION IF NOT EXISTS pg_trgm;

# Verify
\dx

# Exit
\q
```

---

### Issue: Migration Errors

**Symptoms:**
```
django.db.migrations.exceptions.InconsistentMigrationHistory
```

**Solutions:**

**Option 1: Reset migrations (development only):**
```bash
# Backup data first!
python manage.py dumpdata > backup.json

# Drop and recreate database
psql -U postgres
DROP DATABASE django_blog_db;
CREATE DATABASE django_blog_db;
\q

# Run migrations
python manage.py migrate

# Restore data
python manage.py loaddata backup.json
```

**Option 2: Fake migrations:**
```bash
python manage.py migrate --fake blog zero
python manage.py migrate blog
```

---

## Development Server Issues

### Issue: Port Already in Use

**Symptoms:**
```
Error: That port is already in use.
```

**Solutions:**

**Use different port:**
```bash
python manage.py runserver 8001
```

**Find and kill process:**

**Linux/macOS:**
```bash
lsof -i :8000
kill -9 <PID>
```

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### Issue: Server Not Accessible from Network

**Symptoms:**
- Works on localhost but not from other devices

**Solution:**

```bash
# Listen on all interfaces
python manage.py runserver 0.0.0.0:8000

# Add to settings.py
ALLOWED_HOSTS = ['*']  # Development only!
```

---

### Issue: Static Files Not Loading

**Symptoms:**
- CSS/images not displaying
- 404 errors for static files

**Solutions:**

**Development:**
```bash
# Ensure DEBUG = True in settings.py
DEBUG = True

# Check STATIC_URL
STATIC_URL = '/static/'
```

**Production:**
```bash
# Collect static files
python manage.py collectstatic

# Configure web server (Nginx example)
location /static/ {
    alias /path/to/staticfiles/;
}
```

---

## Email Issues

### Issue: Email Not Sending

**Symptoms:**
- No error but email doesn't arrive
- SMTPAuthenticationError

**Solutions:**

**Check .env configuration:**
```bash
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate App Password (not regular password)
3. Use App Password in EMAIL_HOST_PASSWORD

**Test email in shell:**
```python
python manage.py shell

from django.core.mail import send_mail
send_mail(
    'Test Subject',
    'Test message',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

**Use console backend for development:**
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## Admin Interface Issues

### Issue: Cannot Access Admin

**Symptoms:**
- 404 error on /admin/
- Admin login redirects to login page

**Solutions:**

**Verify admin is enabled:**
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',  # Should be present
    # ...
]

# urls.py (foodie/urls.py)
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    # ...
]
```

**Create superuser:**
```bash
python manage.py createsuperuser
```

**Clear browser cache:**
- Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

---

### Issue: Static Files Missing in Admin

**Symptoms:**
- Admin interface has no styling

**Solutions:**

**Development:**
```python
# Ensure DEBUG = True
DEBUG = True
```

**Production:**
```bash
python manage.py collectstatic
```

---

## Template Issues

### Issue: Template Not Found

**Symptoms:**
```
TemplateDoesNotExist: blog/post/list.html
```

**Solutions:**

**Check template path:**
```
blog/templates/blog/post/list.html
```

**Verify APP_DIRS setting:**
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # Should be True
        # ...
    },
]
```

**Verify app is installed:**
```python
INSTALLED_APPS = [
    # ...
    'blog.apps.BlogConfig',  # or just 'blog'
]
```

---

### Issue: Template Variables Not Displaying

**Symptoms:**
- {{ variable }} shows as empty

**Solutions:**

**Check context in view:**
```python
def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {
        'posts': posts  # Ensure variable is in context
    })
```

**Debug in template:**
```django
{{ posts|length }}  {# Shows count #}
{% debug %}  {# Shows all context #}
```

**Check for typos:**
```django
{# Wrong #}
{{ psots }}

{# Correct #}
{{ posts }}
```

---

## Search Issues

### Issue: Search Not Working

**Symptoms:**
- Search returns no results
- SearchQuery error

**Solutions:**

**Ensure pg_trgm extension:**
```bash
psql -U your_username -d django_blog_db
CREATE EXTENSION IF NOT EXISTS pg_trgm;
\q
```

**Run migration:**
```bash
python manage.py migrate blog 0007_trigram_ext
```

**Check search query:**
```python
# In views.py, verify TrigramSimilarity is used correctly
from django.contrib.postgres.search import TrigramSimilarity

results = Post.published.annotate(
    similarity=TrigramSimilarity('title', query)
).filter(similarity__gt=0.1)
```

---

## Performance Issues

### Issue: Slow Page Load Times

**Solutions:**

**Enable query debugging:**
```bash
pip install django-debug-toolbar
```

**Optimize queries:**
```python
# Use select_related for foreign keys
Post.objects.select_related('author').all()

# Use prefetch_related for many-to-many
Post.objects.prefetch_related('tags').all()
```

**Add database indexes:**
```python
class Meta:
    indexes = [
        models.Index(fields=['-publish']),
        models.Index(fields=['slug']),
    ]
```

**Enable caching:**
```bash
pip install redis django-redis
```

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

---

## Security Issues

### Issue: CSRF Verification Failed

**Symptoms:**
```
Forbidden (403): CSRF verification failed
```

**Solutions:**

**Ensure CSRF token in forms:**
```django
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

**Check CSRF_TRUSTED_ORIGINS (production):**
```python
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]
```

---

### Issue: DEBUG = False Shows Error Page

**Symptoms:**
- Generic 500 error page
- No error details

**Solutions:**

**Check error logs:**
```bash
# In your logging configuration
tail -f /var/log/django-blog/django.log
```

**Configure ADMINS:**
```python
ADMINS = [
    ('Your Name', 'your-email@example.com'),
]

# Django will email errors to admins
```

**Use Sentry for production:**
```bash
pip install sentry-sdk
```

---

## Common Python Errors

### ImportError: No module named 'X'

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Install missing package
pip install X

# Or reinstall all requirements
pip install -r requirements.txt
```

---

### SyntaxError or IndentationError

**Solution:**
- Check for proper indentation (4 spaces, not tabs)
- Look for unclosed brackets, quotes
- Use a code editor with Python linting

---

## Getting More Help

### Debug Mode Information

**Enable verbose error pages:**
```python
# settings.py (development only)
DEBUG = True
```

### Django Shell Debugging

```bash
python manage.py shell

# Test queries
from blog.models import Post
Post.objects.all()

# Test imports
from blog.views import post_list

# Test settings
from django.conf import settings
print(settings.DATABASES)
```

### Check Django Setup

```bash
# Check for configuration issues
python manage.py check

# Check specific app
python manage.py check blog
```

### Useful Management Commands

```bash
# Show migrations status
python manage.py showmigrations

# Show SQL for migration
python manage.py sqlmigrate blog 0001

# Validate models
python manage.py validate

# Show database tables
python manage.py dbshell
\dt
```

---

## Still Having Issues?

If your problem isn't covered here:

1. **Check Django Documentation:** [docs.djangoproject.com](https://docs.djangoproject.com/)
2. **Search GitHub Issues:** Existing solutions may be available
3. **Stack Overflow:** Search for similar problems
4. **Open GitHub Issue:** Provide detailed information:
   - Error message and stack trace
   - Steps to reproduce
   - Environment details (OS, Python version, Django version)
   - What you've already tried

---

[← Back to Documentation Index](index.md)
