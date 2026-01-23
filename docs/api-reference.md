# API Reference

This document provides detailed technical reference for models, views, URLs, forms, and template tags in the Django Blog Project.

## Models

### Post Model

**Location:** `blog/models.py`

The primary model for blog posts.

#### Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | AutoField | Primary key | Auto-generated |
| `title` | CharField | Post title | max_length=250, required |
| `slug` | SlugField | URL-friendly identifier | max_length=250, unique_for_date='publish' |
| `author` | ForeignKey | Post author | → User, on_delete=CASCADE |
| `body` | TextField | Post content | required |
| `publish` | DateTimeField | Publication date/time | default=timezone.now |
| `created` | DateTimeField | Creation timestamp | auto_now_add=True |
| `updated` | DateTimeField | Last update timestamp | auto_now=True |
| `status` | CharField | Publication status | max_length=2, choices=Status |
| `tags` | TaggableManager | Associated tags | via django-taggit |

#### Status Choices

```python
class Status(models.TextChoices):
    DRAFT = 'DF', 'Draft'
    PUBLISHED = 'PB', 'Published'
```

#### Managers

**`objects`** - Default Django manager (all posts)
```python
Post.objects.all()  # All posts (draft + published)
```

**`published`** - Custom manager (published posts only)
```python
Post.published.all()  # Only published posts
```

#### Methods

**`get_absolute_url()`**
```python
def get_absolute_url(self):
    return reverse(
        "blog:post_detail",
        args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ]
    )
```

Returns canonical URL for the post.

**Example:** `/post/2026/01/23/my-first-post/`

**`__str__()`**
```python
def __str__(self):
    return self.title
```

Returns string representation (used in admin).

#### Meta Options

```python
class Meta:
    ordering = ['-publish']  # Newest first
    indexes = [
        models.Index(fields=['-publish']),
    ]
```

#### Example Usage

```python
from blog.models import Post
from django.contrib.auth.models import User

# Create a post
user = User.objects.first()
post = Post.objects.create(
    title="My First Post",
    slug="my-first-post",
    author=user,
    body="This is the content...",
    status=Post.Status.PUBLISHED
)

# Query posts
published_posts = Post.published.all()
draft_posts = Post.objects.filter(status=Post.Status.DRAFT)

# Get post by slug
post = Post.published.get(
    slug='my-first-post',
    publish__year=2026,
    publish__month=1,
    publish__day=23
)

# Add tags
post.tags.add("django", "python", "web")

# Get posts by tag
tagged_posts = Post.published.filter(tags__name__in=["django"])
```

---

### Comment Model

**Location:** `blog/models.py`

Model for user comments on blog posts.

#### Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | AutoField | Primary key | Auto-generated |
| `post` | ForeignKey | Associated post | → Post, on_delete=CASCADE |
| `name` | CharField | Commenter's name | max_length=80, required |
| `email` | EmailField | Commenter's email | required |
| `body` | TextField | Comment content | required |
| `created` | DateTimeField | Creation timestamp | auto_now_add=True |
| `updated` | DateTimeField | Last update timestamp | auto_now=True |
| `active` | BooleanField | Moderation status | default=True |

#### Related Name

Access comments from post:
```python
post.comments.all()  # All comments for post
post.comments.filter(active=True)  # Active comments only
```

#### Methods

**`__str__()`**
```python
def __str__(self):
    return f'Commented by {self.name} on {self.post}'
```

#### Meta Options

```python
class Meta:
    ordering = ['created']  # Oldest first
    indexes = [
        models.Index(fields=['created']),
    ]
```

#### Example Usage

```python
from blog.models import Post, Comment

post = Post.published.first()

# Create comment
comment = Comment.objects.create(
    post=post,
    name="John Doe",
    email="john@example.com",
    body="Great post!",
    active=True
)

# Get all comments for post
comments = post.comments.all()
active_comments = post.comments.filter(active=True)

# Moderate comment
comment.active = False
comment.save()
```

---

## Views

### post_list

**Location:** `blog/views.py`

Display paginated list of published posts, optionally filtered by tag.

#### Signature

```python
def post_list(request, tag_slug=None):
```

#### Parameters

- `request` (HttpRequest): The request object
- `tag_slug` (str, optional): Tag slug to filter posts

#### Returns

HttpResponse with rendered template

#### Template

`blog/post/list.html`

#### Context

```python
{
    'posts': QuerySet[Post],      # All posts (for context)
    'page_obj': Page,              # Current page of posts
    'tag': Tag or None             # Current tag filter
}
```

#### URL Patterns

```python
path('post/', views.post_list, name='post_list')
path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag')
```

#### Example

```python
# View all posts
http://127.0.0.1:8000/post/
http://127.0.0.1:8000/post/?page=2

# Filter by tag
http://127.0.0.1:8000/tag/django/
```

---

### Post_detail

**Location:** `blog/views.py`

Display a single blog post with comments and similar posts.

#### Signature

```python
def Post_detail(request, year, month, day, post):
```

#### Parameters

- `request` (HttpRequest): The request object
- `year` (int): Publication year
- `month` (int): Publication month
- `day` (int): Publication day
- `post` (str): Post slug

#### Returns

HttpResponse with rendered template

#### Template

`blog/post/detail.html`

#### Context

```python
{
    'post': Post,                  # The blog post
    'comments': QuerySet[Comment], # Active comments (limited)
    'total_comments': int,         # Total comment count
    'has_more_comments': bool,     # More comments available
    'next_comment_limit': int,     # Next limit for "load more"
    'comment_limit': int,          # Current limit
    'form': CommentForm,           # Comment submission form
    'similar_posts': QuerySet[Post] # Related posts (max 4)
}
```

#### URL Pattern

```python
path(
    'post/<int:year>/<int:month>/<int:day>/<slug:post>/',
    views.Post_detail,
    name='post_detail'
)
```

#### Example

```python
http://127.0.0.1:8000/post/2026/01/23/my-first-post/
http://127.0.0.1:8000/post/2026/01/23/my-first-post/?climit=10
```

---

### post_share

**Location:** `blog/views.py`

Share a blog post via email.

#### Signature

```python
def post_share(request, post_id):
```

#### Parameters

- `request` (HttpRequest): The request object
- `post_id` (int): Post ID

#### Returns

HttpResponse with rendered template

#### Template

`blog/post/share.html`

#### Context

```python
{
    'post': Post,           # The blog post
    'form': EmailPostForm,  # Sharing form
    'sent': bool            # Email sent successfully
}
```

#### URL Pattern

```python
path('<int:post_id>/share/', views.post_share, name='post_share')
```

---

### post_comment

**Location:** `blog/views.py`

Handle comment submission (POST only).

#### Signature

```python
@require_POST
def post_comment(request, post_id):
```

#### Decorators

- `@require_POST` - Only accepts POST requests

#### Parameters

- `request` (HttpRequest): The request object
- `post_id` (int): Post ID

#### Returns

HttpResponse with rendered template

#### Template

`blog/post/comment.html`

#### Context

```python
{
    'post': Post,           # The blog post
    'form': CommentForm,    # Comment form (validated)
    'comment': Comment      # Created comment (if valid)
}
```

#### URL Pattern

```python
path('<int:post_id>/comment/', views.post_comment, name='post_comment')
```

---

### post_search

**Location:** `blog/views.py`

Search posts using PostgreSQL trigram similarity.

#### Signature

```python
def post_search(request):
```

#### Parameters

- `request` (HttpRequest): The request object

#### Returns

HttpResponse with rendered template

#### Template

`blog/post/search.html`

#### Context

```python
{
    'form': SearchForm,         # Search form
    'query': str or None,       # Search query
    'results': QuerySet[Post]   # Search results
}
```

#### URL Pattern

```python
path('search/', views.post_search, name='post_search')
```

#### Example

```python
http://127.0.0.1:8000/search/?query=django
```

---

### home

**Location:** `blog/views.py`

Display homepage.

#### Signature

```python
def home(request):
```

#### Template

`blog/post/home.html`

#### URL Pattern

```python
path('', views.home, name='home')
```

---

## Forms

### EmailPostForm

**Location:** `blog/form.py`

Form for sharing posts via email.

#### Fields

```python
name = forms.CharField(max_length=25)
email = forms.EmailField()
to = forms.EmailField()
comments = forms.CharField(required=False, widget=forms.Textarea)
```

#### Usage

```python
form = EmailPostForm(request.POST)
if form.is_valid():
    cd = form.cleaned_data
    # Access: cd['name'], cd['email'], cd['to'], cd['comments']
```

---

### CommentForm

**Location:** `blog/form.py`

ModelForm for submitting comments.

#### Fields

Based on Comment model (name, email, body).

#### Usage

```python
form = CommentForm(data=request.POST)
if form.is_valid():
    comment = form.save(commit=False)
    comment.post = post
    comment.save()
```

---

### SearchForm

**Location:** `blog/form.py`

Form for searching posts.

#### Fields

```python
query = forms.CharField()
```

#### Usage

```python
form = SearchForm(request.GET)
if form.is_valid():
    query = form.cleaned_data['query']
```

---

## URL Patterns

**Location:** `blog/urls.py`

**App Name:** `blog`

### URL Configuration

```python
urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.Post_detail, name='post_detail'),
    path('kiya/', views.kiya_view, name='kiya'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]
```

### Reverse URL Resolution

In Python:
```python
from django.urls import reverse

url = reverse('blog:post_list')
url = reverse('blog:post_detail', args=[2026, 1, 23, 'my-post'])
url = reverse('blog:post_list_by_tag', args=['django'])
```

In Templates:
```django
{% url 'blog:post_list' %}
{% url 'blog:post_detail' post.publish.year post.publish.month post.publish.day post.slug %}
{% url 'blog:post_list_by_tag' tag.slug %}
```

---

## Feeds

### LatestPostsFeed

**Location:** `blog/feeds.py`

RSS feed for latest blog posts.

#### Methods

**`title()`** - Feed title
**`link()`** - Feed URL
**`description()`** - Feed description
**`items()`** - QuerySet of items to include

#### URL

```python
path('feed/', LatestPostsFeed(), name='post_feed')
```

#### Access

```
http://127.0.0.1:8000/feed/
```

---

## Sitemaps

**Location:** `blog/sitemaps.py`

XML sitemap for SEO.

---

## Template Tags

**Location:** `blog/templatetags/blog_tags.py`

Custom template tags for the blog app.

### Loading Tags

```django
{% load blog_tags %}
```

### Available Tags

Document any custom tags created in `blog_tags.py`.

---

## Admin

### PostAdmin

**Location:** `blog/admin.py`

Customized admin for Post model.

#### Configuration

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    search_fields = ['title', 'body']
```

---

### CommentAdmin

**Location:** `blog/admin.py`

Customized admin for Comment model.

#### Configuration

```python
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
```

---

## QuerySet Examples

### Common Queries

```python
# Get all published posts
Post.published.all()

# Get posts from specific year
Post.published.filter(publish__year=2026)

# Get posts by author
user = User.objects.get(username='john')
user.blog_posts.all()

# Get posts with tag
Post.published.filter(tags__name__in=['django'])

# Get posts with comment count
from django.db.models import Count
Post.published.annotate(comment_count=Count('comments'))

# Search posts
from django.contrib.postgres.search import TrigramSimilarity
Post.published.annotate(
    similarity=TrigramSimilarity('title', 'django')
).filter(similarity__gt=0.1)

# Get similar posts
post_tags = post.tags.values_list('id', flat=True)
similar = Post.published.filter(tags__in=post_tags).exclude(id=post.id)
similar = similar.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
```

---

## Next Steps

- **[Development Guide](development.md)** - Development workflows
- **[Troubleshooting](troubleshooting.md)** - Common issues
- **[Contributing](contributing.md)** - Contribution guidelines

---

[← Back to Documentation Index](index.md)
