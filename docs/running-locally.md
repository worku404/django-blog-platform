# Running Locally

This guide covers how to run and work with the Django Blog Project in your local development environment.

---

## Starting the Development Server

### Basic Server Start

Navigate to the project directory and activate your virtual environment:

```bash
cd gold_blog
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

Start the Django development server:

```bash
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000/**

### Custom Port

To run on a different port:

```bash
python manage.py runserver 8080
python manage.py runserver 0.0.0.0:8000  # Accessible from network
```

### Auto-Reload

The development server automatically reloads when you change Python files. You don't need to restart manually for most changes.

---

## Accessing the Application

### Main URLs

Once the server is running:

- **Homepage**: http://127.0.0.1:8000/
- **Blog Post List**: http://127.0.0.1:8000/post/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Search**: http://127.0.0.1:8000/search/
- **RSS Feed**: http://127.0.0.1:8000/feed/

### First-Time Access

On first access, you may see an empty blog. You need to:
1. Log into the admin panel
2. Create your first post
3. Set it to "Published" status

---

## Development Workflow

### 1. Making Changes

#### Code Changes

Edit files using your preferred editor:

```bash
# Edit models
code blog/models.py

# Edit views
code blog/views.py

# Edit templates
code blog/templates/blog/post/list.html
```

**Note:** Python changes auto-reload, but template changes may need a browser refresh.

#### CSS Changes

Edit CSS files:

```bash
code blog/static/blog/css/blog.css
```

**Note:** You may need to hard-refresh your browser (Ctrl+F5 or Cmd+Shift+R) to see CSS changes.

### 2. Database Changes

When you modify models:

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View SQL that will be executed
python manage.py sqlmigrate blog 0001
```

### 3. Testing Changes

#### Manual Testing

1. Navigate to the affected page
2. Test the functionality
3. Check the terminal for error messages
4. Review Django Debug Toolbar (if installed)

#### Creating Test Data

Use the Django shell to create test data:

```bash
python manage.py shell
```

```python
from blog.models import Post
from django.contrib.auth.models import User

# Get or create a user
author = User.objects.first()

# Create a test post
post = Post.objects.create(
    title="Test Post",
    slug="test-post",
    author=author,
    body="This is test content.",
    status=Post.Status.PUBLISHED
)

print(f"Created post: {post.title}")
```

---

## Common Development Tasks

### Viewing Logs

The development server prints all requests and errors to the console:

```
[23/Jan/2026 10:30:45] "GET /post/ HTTP/1.1" 200 4532
[23/Jan/2026 10:30:46] "GET /static/blog/css/blog.css HTTP/1.1" 304 0
```

### Database Management

#### View Database Contents

```bash
python manage.py dbshell
```

```sql
-- List all posts
SELECT id, title, status FROM blog_post;

-- Count posts
SELECT COUNT(*) FROM blog_post WHERE status = 'PB';
```

#### Reset Database

⚠️ **Warning: This deletes all data!**

```bash
# For SQLite
rm db.sqlite3
python manage.py migrate

# For PostgreSQL
python manage.py flush
```

### Creating Superuser

Create additional admin users:

```bash
python manage.py createsuperuser
```

### Running Django Shell

Access Django's interactive shell:

```bash
python manage.py shell
```

Useful for:
- Testing queries
- Creating test data
- Debugging code
- Exploring the ORM

Example session:

```python
from blog.models import Post
from django.utils import timezone

# Get all published posts
posts = Post.published.all()
print(f"Found {posts.count()} published posts")

# Get posts from last 7 days
from datetime import timedelta
recent = Post.published.filter(
    publish__gte=timezone.now() - timedelta(days=7)
)
print(f"Recent posts: {recent.count()}")
```

---

## Static Files in Development

### How Static Files Work

Django serves static files automatically in development when:
1. `DEBUG = True`
2. `django.contrib.staticfiles` is in `INSTALLED_APPS`

### Troubleshooting Static Files

If CSS/images don't load:

1. **Check template tags:**
```django
{% load static %}
<link rel="stylesheet" href="{% static 'blog/css/blog.css' %}">
```

2. **Verify file exists:**
```bash
ls blog/static/blog/css/blog.css
```

3. **Check settings:**
```python
STATIC_URL = '/static/'
```

4. **Hard refresh browser** (Ctrl+F5)

---

## Debugging Tips

### Enable Verbose Error Pages

Ensure `DEBUG = True` in settings.py for detailed error pages.

### Use Print Statements

Add print statements in views:

```python
def post_list(request):
    posts = Post.published.all()
    print(f"Found {posts.count()} posts")  # Shows in console
    return render(request, 'blog/post/list.html', {'posts': posts})
```

### Django Debug Toolbar (Optional)

Install for advanced debugging:

```bash
pip install django-debug-toolbar
```

Add to settings:

```python
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]

INTERNAL_IPS = [
    '127.0.0.1',
]
```

### Check Query Performance

In shell:

```python
from django.db import connection
from blog.models import Post

posts = list(Post.published.all())
print(connection.queries)  # See all SQL queries
```

---

## Working with Fixtures

### Export Data

Save current data to a JSON file:

```bash
python manage.py dumpdata blog.Post --indent 2 > posts.json
python manage.py dumpdata blog > blog_data.json
```

### Import Data

Load data from a JSON file:

```bash
python manage.py loaddata posts.json
python manage.py loaddata mysite_data.json
```

Useful for:
- Sharing sample data
- Backing up data
- Resetting to a known state

---

## Email Testing in Development

### Console Email Backend

In `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Emails will print to your console instead of sending.

### File-Based Email Backend

Save emails as files:

```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'tmp' / 'emails'
```

Emails saved to `tmp/emails/` directory.

### Test Email Sending

In Django shell:

```python
from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message body',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

---

## Database Switching

### Switch to SQLite

For quick local testing, edit `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Then migrate:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Switch Back to PostgreSQL

Restore PostgreSQL settings and migrate:

```bash
python manage.py migrate --database=default
```

---

## Performance Monitoring

### Django Debug Toolbar

Shows:
- SQL queries executed
- Template rendering time
- Cache hits/misses
- Request/response data

### Manual Query Counting

```python
from django.db import reset_queries, connection

reset_queries()
# ... run your code ...
print(f"Queries executed: {len(connection.queries)}")
```

### Template Performance

Add timing in templates:

```django
{% load static %}
{% now "Y-m-d H:i:s" as current_time %}
<!-- Rendered at {{ current_time }} -->
```

---

## Common Issues & Solutions

### Port Already in Use

```bash
# Kill process on port 8000 (Linux/Mac)
lsof -ti:8000 | xargs kill -9

# Or use different port
python manage.py runserver 8080
```

### Migration Conflicts

```bash
# Show migration status
python manage.py showmigrations

# Fake a migration if needed
python manage.py migrate blog --fake 0001

# Or reset migrations (careful!)
python manage.py migrate blog zero
rm blog/migrations/000*.py
python manage.py makemigrations blog
python manage.py migrate
```

### Database Locked (SQLite)

Stop all `manage.py` processes and try again. SQLite doesn't handle concurrent access well.

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check virtual environment is activated
which python  # Should show venv path
```

---

## Git Workflow

### Before Making Changes

```bash
git status
git pull origin main
git checkout -b feature/my-new-feature
```

### After Making Changes

```bash
git status
git add .
git commit -m "Add new feature"
git push origin feature/my-new-feature
```

### View Changes

```bash
git diff
git diff --staged
git log --oneline
```

---

## Shutting Down

### Stop the Server

Press **Ctrl+C** in the terminal running the server.

### Deactivate Virtual Environment

```bash
deactivate
```

### Check for Running Processes

```bash
# See if server is still running
lsof -ti:8000

# Or
ps aux | grep python
```

---

## Development Checklist

Daily workflow:

- [ ] Activate virtual environment
- [ ] Pull latest changes from git
- [ ] Check for new dependencies (`pip install -r requirements.txt`)
- [ ] Run migrations (`python manage.py migrate`)
- [ ] Start development server
- [ ] Make changes
- [ ] Test locally
- [ ] Commit changes
- [ ] Push to repository

---

[← Back to Documentation Index](README.md)
