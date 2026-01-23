# Development Guide

This guide covers development workflows, testing practices, and best practices for contributing to the Django Blog Project.

## Development Environment Setup

### Prerequisites

Ensure you've completed the [Installation Guide](installation.md) before proceeding.

### Recommended Tools

**Code Editor:**
- **VS Code** with Python extension
- **PyCharm** (Community or Professional)
- **Sublime Text** with Python packages

**Database Tools:**
- **pgAdmin** - PostgreSQL GUI
- **DBeaver** - Universal database tool
- **psql** - PostgreSQL command-line

**Version Control:**
- **Git** - Version control system
- **GitHub Desktop** - GUI for Git (optional)

### IDE Configuration

#### VS Code Settings

Install extensions:
- Python (Microsoft)
- Django Template
- Pylint
- Black Formatter

**settings.json:**
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.languageServer": "Pylance",
    "[python]": {
        "editor.formatOnSave": true
    }
}
```

#### PyCharm Configuration

1. Set interpreter to your virtual environment
2. Enable Django support:
   - Settings → Languages & Frameworks → Django
   - Enable Django Support
   - Django project root: `/path/to/gold_blog`
   - Settings: `foodie/settings.py`
   - Manage script: `manage.py`

## Development Workflow

### Starting Development

1. **Activate virtual environment:**
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

2. **Navigate to project:**
```bash
cd gold_blog
```

3. **Start development server:**
```bash
python manage.py runserver
```

4. **Access development server:**
```
http://127.0.0.1:8000/
```

### Making Changes

#### Modifying Models

1. Edit `blog/models.py`
2. Create migrations:
```bash
python manage.py makemigrations
```
3. Review migration file in `blog/migrations/`
4. Apply migrations:
```bash
python manage.py migrate
```

**Example: Adding a field**
```python
# blog/models.py
class Post(models.Model):
    # ... existing fields
    reading_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
```

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Modifying Views

1. Edit `blog/views.py`
2. Update URL patterns if needed in `blog/urls.py`
3. Update templates in `blog/templates/blog/`
4. Test in browser

**Example: Adding a view**
```python
# blog/views.py
def about(request):
    return render(request, 'blog/post/about.html')

# blog/urls.py
urlpatterns = [
    # ...
    path('about/', views.about, name='about'),
]
```

#### Modifying Templates

1. Edit files in `blog/templates/blog/`
2. Use template inheritance
3. Reload browser (auto-updates with runserver)

**Template Structure:**
```django
{% extends "blog/base.html" %}

{% block content %}
    <!-- Your content here -->
{% endblock %}
```

#### Modifying Static Files

1. Edit CSS/JS in `blog/static/blog/`
2. Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
3. In production, run `collectstatic`

### Testing Changes

#### Manual Testing

1. Browse to affected pages
2. Test all user interactions
3. Check different browsers
4. Test responsive design (mobile/tablet)
5. Verify data persistence

#### Django Shell

Test models and queries interactively:

```bash
python manage.py shell
```

```python
>>> from blog.models import Post, Comment
>>> from django.contrib.auth.models import User

# Query posts
>>> Post.objects.all()
>>> Post.published.all()
>>> Post.objects.filter(status=Post.Status.PUBLISHED)

# Create a post
>>> user = User.objects.first()
>>> post = Post.objects.create(
...     title="Test Post",
...     slug="test-post",
...     author=user,
...     body="Test content",
...     status=Post.Status.PUBLISHED
... )

# Query with annotations
>>> from django.db.models import Count
>>> Post.published.annotate(comment_count=Count('comments'))
```

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test blog

# Run specific test class
python manage.py test blog.tests.PostModelTest

# Run with verbosity
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

### Writing Tests

Create tests in `blog/tests.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment

class PostModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='Test content',
            status=Post.Status.PUBLISHED
        )
    
    def test_post_creation(self):
        """Test post is created correctly"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.slug, 'test-post')
        self.assertEqual(self.post.status, Post.Status.PUBLISHED)
    
    def test_post_str(self):
        """Test post string representation"""
        self.assertEqual(str(self.post), 'Test Post')
    
    def test_get_absolute_url(self):
        """Test post URL generation"""
        url = self.post.get_absolute_url()
        self.assertIn('/post/', url)
        self.assertIn('test-post', url)

class PostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='Test content',
            status=Post.Status.PUBLISHED
        )
    
    def test_post_list_view(self):
        """Test post list page loads"""
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_post_detail_view(self):
        """Test post detail page loads"""
        url = self.post.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test content')
```

### Test Coverage

Install coverage:
```bash
pip install coverage
```

Run with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

View report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Code Quality

### Linting with Pylint

Install:
```bash
pip install pylint
```

Run:
```bash
pylint blog/
```

### Formatting with Black

Install:
```bash
pip install black
```

Format code:
```bash
black blog/
black --check blog/  # Check without modifying
```

### Type Checking with mypy

Install:
```bash
pip install mypy
```

Run:
```bash
mypy blog/
```

### Pre-commit Hooks

Install pre-commit:
```bash
pip install pre-commit
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

Install hooks:
```bash
pre-commit install
```

## Database Management

### Accessing Database

**Django Shell:**
```bash
python manage.py dbshell
```

**PostgreSQL Command Line:**
```bash
psql -U blog_user -d django_blog_db
```

### Database Commands

```sql
-- List tables
\dt

-- Describe table
\d blog_post

-- Query posts
SELECT id, title, status FROM blog_post;

-- Count comments
SELECT COUNT(*) FROM blog_comment;
```

### Backup and Restore

**Backup:**
```bash
python manage.py dumpdata > backup.json
python manage.py dumpdata blog > blog_backup.json
```

**Restore:**
```bash
python manage.py loaddata backup.json
```

**PostgreSQL Backup:**
```bash
pg_dump django_blog_db > backup.sql
```

**PostgreSQL Restore:**
```bash
psql django_blog_db < backup.sql
```

### Reset Database

```bash
# Drop and recreate database
psql -U postgres
DROP DATABASE django_blog_db;
CREATE DATABASE django_blog_db;
\q

# Reapply migrations
python manage.py migrate
python manage.py createsuperuser
```

## Debugging

### Django Debug Toolbar

Install:
```bash
pip install django-debug-toolbar
```

Configure:
```python
# settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# urls.py
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

### Print Debugging

```python
# In views.py
def post_list(request):
    posts = Post.published.all()
    print(f"Number of posts: {posts.count()}")  # Debug output
    print(f"SQL Query: {posts.query}")
    return render(request, 'blog/post/list.html', {'posts': posts})
```

### Logging

```python
# views.py
import logging

logger = logging.getLogger(__name__)

def post_detail(request, year, month, day, post):
    logger.info(f"Accessing post: {post}")
    # ... rest of view
```

### Interactive Debugger

Use `pdb`:
```python
def post_detail(request, year, month, day, post):
    import pdb; pdb.set_trace()  # Breakpoint
    post = get_object_or_404(Post, slug=post)
    # ...
```

Commands:
- `n` - Next line
- `s` - Step into
- `c` - Continue
- `p variable` - Print variable
- `q` - Quit

## Best Practices

### Code Organization

- **Keep views simple**: Business logic in models/utils
- **DRY principle**: Don't repeat yourself
- **Template inheritance**: Use base templates
- **URL naming**: Always use named URLs
- **Reverse URLs**: Use `reverse()` or `{% url %}`

### Django Conventions

- **Model names**: Singular (Post, not Posts)
- **View names**: Descriptive (post_list, not list)
- **Template names**: Match view/model (post_list.html)
- **URL patterns**: RESTful when possible

### Security

- **Never commit secrets**: Use `.env`
- **Validate input**: Use Django forms
- **Escape output**: Django does this by default
- **Use CSRF protection**: Enabled by default
- **SQL injection**: Use ORM, not raw SQL

### Performance

- **Select related**: Reduce queries
```python
Post.objects.select_related('author').all()
```

- **Prefetch related**: For many-to-many
```python
Post.objects.prefetch_related('tags').all()
```

- **Index database fields**: Add indexes in Meta
- **Cache views**: Use Django's caching
- **Optimize queries**: Use `django-debug-toolbar`

## Version Control

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request on GitHub
```

### Commit Messages

Follow conventional commits:
```
feat: Add comment pagination
fix: Resolve email sending issue
docs: Update installation guide
style: Format code with black
refactor: Simplify post query logic
test: Add tests for comment model
```

### .gitignore

Ensure these are ignored:
```
.env
*.pyc
__pycache__/
db.sqlite3
staticfiles/
media/
venv/
.vscode/
.idea/
```

## Documentation

### Docstrings

```python
def post_list(request, tag_slug=None):
    """
    Display a paginated list of published blog posts.
    
    Args:
        request: HTTP request object
        tag_slug: Optional slug to filter posts by tag
    
    Returns:
        HttpResponse with rendered template
    """
    # ... implementation
```

### Comments

```python
# Good comments explain WHY, not WHAT
# Calculate similarity to find related posts
similar_posts = Post.published.filter(tags__in=post_tag_ids)

# Bad comments repeat the code
# Loop through posts
for post in posts:
    ...
```

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/django.yml`:

```yaml
name: Django CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python manage.py test
```

## Next Steps

- **[API Reference](api-reference.md)** - Detailed code reference
- **[Deployment Guide](deployment.md)** - Deploy to production
- **[Contributing Guidelines](contributing.md)** - Contribute to the project

---

[← Back to Documentation Index](index.md) | [Next: API Reference →](api-reference.md)
