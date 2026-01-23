# Customization

This guide shows you how to customize and extend the Django Blog Project to meet your specific needs.

---

## Customizing the Appearance

### Modifying CSS Styles

#### Global Styles

Edit `blog/static/blog/css/blog.css` for site-wide changes:

```css
/* Change color scheme */
:root {
    --primary-color: #3498db;
    --text-color: #333;
    --background-color: #fff;
}

/* Modify typography */
body {
    font-family: 'Your Font', sans-serif;
    font-size: 18px;
    line-height: 1.8;
}

/* Update link colors */
a {
    color: var(--primary-color);
}
```

#### Page-Specific Styles

Each page has its own CSS file:

**Post List** - `blog/static/blog/css/list.css`
```css
.post-list-item {
    background-color: #f9f9f9;
    padding: 20px;
    margin-bottom: 20px;
}
```

**Post Detail** - `blog/static/blog/css/detail.css`
```css
.post-detail {
    max-width: 800px;
    margin: 0 auto;
}
```

**Homepage** - `blog/static/blog/css/home.css`
```css
.hero-section {
    background: linear-gradient(to right, #667eea, #764ba2);
    padding: 60px 20px;
}
```

#### Adding Custom Fonts

In your CSS file:

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

body {
    font-family: 'Inter', sans-serif;
}
```

Or download and add fonts locally:

```css
@font-face {
    font-family: 'CustomFont';
    src: url('../fonts/customfont.woff2') format('woff2');
}
```

---

## Customizing Templates

### Modifying Existing Templates

Templates are in `blog/templates/blog/`

#### Example: Customize Post List

Edit `blog/templates/blog/post/list.html`:

```django
{% extends "blog/base.html" %}
{% load static %}

{% block title %}Blog Posts{% endblock %}

{% block content %}
<div class="post-list">
    <h1>Latest Articles</h1>  <!-- Custom heading -->
    
    {% for post in page_obj %}
    <article class="post-item">
        <!-- Add featured image -->
        {% if post.featured_image %}
        <img src="{{ post.featured_image.url }}" alt="{{ post.title }}">
        {% endif %}
        
        <h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2>
        
        <!-- Add excerpt -->
        <p class="excerpt">{{ post.body|truncatewords:30 }}</p>
        
        <!-- Add read time -->
        <span class="read-time">{{ post.body|wordcount|reading_time }} min read</span>
        
        <!-- Existing content -->
        <div class="meta">
            <span class="author">By {{ post.author }}</span>
            <span class="date">{{ post.publish|date:"F d, Y" }}</span>
        </div>
        
        <!-- Tags -->
        <div class="tags">
            {% for tag in post.tags.all %}
            <a href="{% url 'blog:post_list_by_tag' tag.slug %}" class="tag">
                #{{ tag.name }}
            </a>
            {% endfor %}
        </div>
    </article>
    {% endfor %}
</div>
{% endblock %}
```

#### Example: Customize Base Template

Edit `blog/templates/blog/base.html`:

```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %} - My Blog</title>
    
    <!-- Add custom meta tags -->
    <meta name="description" content="{% block meta_description %}A Django blog{% endblock %}">
    <meta name="author" content="Your Name">
    
    {% load static %}
    <link rel="stylesheet" href="{% static 'blog/css/blog.css' %}">
    
    <!-- Add favicon -->
    <link rel="icon" href="{% static 'blog/image/favicon.ico' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Add custom navigation -->
    <nav class="main-nav">
        <div class="container">
            <a href="{% url 'blog:home' %}" class="logo">My Blog</a>
            <ul class="nav-links">
                <li><a href="{% url 'blog:home' %}">Home</a></li>
                <li><a href="{% url 'blog:post_list' %}">Blog</a></li>
                <li><a href="{% url 'blog:post_search' %}">Search</a></li>
                <li><a href="/about/">About</a></li>
            </ul>
        </div>
    </nav>
    
    <main class="content">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Custom footer -->
    <footer class="site-footer">
        <p>&copy; {% now "Y" %} Your Name. All rights reserved.</p>
        <p><a href="{% url 'blog:post_feed' %}">RSS Feed</a></p>
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## Adding New Features

### Adding Categories

#### 1. Create Category Model

Edit `blog/models.py`:

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:post_list_by_category', args=[self.slug])

# Add to Post model
class Post(models.Model):
    # ... existing fields ...
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
```

#### 2. Create and Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3. Register in Admin

Edit `blog/admin.py`:

```python
from .models import Post, Comment, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
```

#### 4. Add URL Pattern

Edit `blog/urls.py`:

```python
urlpatterns = [
    # ... existing patterns ...
    path(
        'category/<slug:category_slug>/',
        views.post_list_by_category,
        name='post_list_by_category'
    ),
]
```

#### 5. Create View

Edit `blog/views.py`:

```python
def post_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.published.filter(category=category)
    
    from django.core.paginator import Paginator
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'blog/post/list.html',
        {
            'posts': posts,
            'page_obj': page_obj,
            'category': category
        }
    )
```

### Adding Featured Images

#### 1. Install Pillow

```bash
pip install Pillow
echo "Pillow" >> requirements.txt
```

#### 2. Configure Media Files

Edit `foodie/settings.py`:

```python
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Edit `foodie/urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... existing patterns ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### 3. Add Image Field to Model

Edit `blog/models.py`:

```python
class Post(models.Model):
    # ... existing fields ...
    featured_image = models.ImageField(
        upload_to='posts/%Y/%m/%d/',
        blank=True,
        null=True
    )
```

#### 4. Migrate

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Update Templates

In `blog/templates/blog/post/detail.html`:

```django
{% if post.featured_image %}
<div class="featured-image">
    <img src="{{ post.featured_image.url }}" alt="{{ post.title }}">
</div>
{% endif %}
```

### Adding Rich Text Editor

#### Using Django-CKEditor

1. **Install**

```bash
pip install django-ckeditor
```

2. **Configure**

Add to `settings.py`:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    'ckeditor',
    'ckeditor_uploader',
]

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}
```

3. **Update Model**

```python
from ckeditor.fields import RichTextField

class Post(models.Model):
    # Replace body field
    body = RichTextField()
```

4. **Migrate**

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Custom Template Tags

### Creating Custom Template Tags

Create `blog/templatetags/blog_tags.py`:

```python
from django import template
from blog.models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter
def reading_time(word_count):
    """Calculate reading time in minutes (200 words per minute)"""
    return max(1, round(word_count / 200))
```

### Using Custom Template Tags

In your templates:

```django
{% load blog_tags %}

<!-- Use simple tag -->
<p>Total posts: {% total_posts %}</p>

<!-- Use inclusion tag -->
{% show_latest_posts 3 %}

<!-- Use filter -->
<span>{{ post.body|wordcount|reading_time }} min read</span>
```

---

## Adding Social Media Sharing

### Share Buttons

Create `blog/templates/blog/post/includes/social_share.html`:

```django
<div class="social-share">
    <h3>Share this post:</h3>
    
    <!-- Twitter -->
    <a href="https://twitter.com/intent/tweet?text={{ post.title }}&url={{ request.build_absolute_uri }}" 
       target="_blank" class="share-btn twitter">
        Share on Twitter
    </a>
    
    <!-- Facebook -->
    <a href="https://www.facebook.com/sharer/sharer.php?u={{ request.build_absolute_uri }}" 
       target="_blank" class="share-btn facebook">
        Share on Facebook
    </a>
    
    <!-- LinkedIn -->
    <a href="https://www.linkedin.com/shareArticle?mini=true&url={{ request.build_absolute_uri }}&title={{ post.title }}" 
       target="_blank" class="share-btn linkedin">
        Share on LinkedIn
    </a>
    
    <!-- Copy Link -->
    <button onclick="copyToClipboard('{{ request.build_absolute_uri }}')" class="share-btn copy">
        Copy Link
    </button>
</div>

<script>
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Link copied to clipboard!');
    });
}
</script>
```

Include in `detail.html`:

```django
{% include 'blog/post/includes/social_share.html' %}
```

---

## Customizing Admin Interface

### Custom Admin Theme

Install Django Admin Interface:

```bash
pip install django-admin-interface
```

Add to `settings.py`:

```python
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    # ... other apps ...
]
```

Configure in admin interface settings page.

### Custom Admin Actions

Edit `blog/admin.py`:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # ... existing config ...
    
    actions = ['make_published', 'make_draft']
    
    @admin.action(description='Mark selected posts as published')
    def make_published(self, request, queryset):
        updated = queryset.update(status=Post.Status.PUBLISHED)
        self.message_user(request, f'{updated} posts marked as published.')
    
    @admin.action(description='Mark selected posts as draft')
    def make_draft(self, request, queryset):
        updated = queryset.update(status=Post.Status.DRAFT)
        self.message_user(request, f'{updated} posts marked as draft.')
```

---

## Performance Optimizations

### Database Query Optimization

Edit `blog/views.py`:

```python
def post_list(request, tag_slug=None):
    # Use select_related for foreign keys
    post_list = Post.published.select_related('author').all()
    
    # Use prefetch_related for many-to-many
    post_list = post_list.prefetch_related('tags')
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    # ... rest of view ...
```

### Template Fragment Caching

In templates:

```django
{% load cache %}

{% cache 500 sidebar %}
    <!-- Cached for 500 seconds -->
    {% show_latest_posts 5 %}
{% endcache %}
```

### Enable Database Caching

In `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
```

Create cache table:

```bash
python manage.py createcachetable
```

---

## Adding User Authentication

### Enable User Registration

Install django-allauth:

```bash
pip install django-allauth
```

Configure in `settings.py`:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

Add URLs:

```python
urlpatterns = [
    # ... existing patterns ...
    path('accounts/', include('allauth.urls')),
]
```

---

## Internationalization

### Enable Multiple Languages

In `settings.py`:

```python
from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fr', _('French')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
```

Mark strings for translation:

```python
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    title = models.CharField(_('title'), max_length=250)
```

Create translation files:

```bash
python manage.py makemessages -l es
python manage.py compilemessages
```

---

## Additional Customizations

### Custom 404 Page

Create `templates/404.html`:

```django
{% extends "blog/base.html" %}

{% block content %}
<div class="error-page">
    <h1>Page Not Found</h1>
    <p>Sorry, the page you're looking for doesn't exist.</p>
    <a href="{% url 'blog:home' %}">Go to Homepage</a>
</div>
{% endblock %}
```

Set `DEBUG = False` and configure `ALLOWED_HOSTS` to test.

### Adding Analytics

In `base.html`:

```django
{% if not debug %}
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
{% endif %}
```

---

[← Back to Documentation Index](README.md)
