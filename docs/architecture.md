# Architecture

This document describes the technical architecture and design decisions of the Django Blog Project.

---

## System Overview

The Django Blog Project follows a traditional **MVC (Model-View-Controller)** pattern, or more specifically, Django's **MTV (Model-Template-View)** architecture.

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────┐
│   Django    │
│  URL Router │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│    Views    │◄────►│  Templates   │
└──────┬──────┘      └──────────────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│   Models    │◄────►│  Database    │
└─────────────┘      └──────────────┘
```

---

## Application Structure

### Django Project: `foodie`

The main Django project container that provides:
- Global settings (`settings.py`)
- URL routing configuration (`urls.py`)
- WSGI/ASGI application entry points
- Environment configuration management

### Django App: `blog`

The core application containing all blogging functionality:
- Models for data structure
- Views for business logic
- Templates for presentation
- Static files for styling
- URL patterns for routing
- Admin configurations

---

## Data Layer (Models)

### Post Model

The central model representing a blog post:

```python
Post
├── title: CharField          # Post title
├── slug: SlugField          # URL-friendly identifier
├── author: ForeignKey       # Link to Django User
├── body: TextField          # Post content
├── publish: DateTimeField   # Publication date/time
├── created: DateTimeField   # Creation timestamp
├── updated: DateTimeField   # Last update timestamp
├── status: CharField        # DRAFT or PUBLISHED
└── tags: TaggableManager    # Tags via django-taggit
```

**Key Features:**
- **Custom Manager (`PublishedManager`)** - Filters only published posts
- **Unique Slug Constraint** - Slugs are unique per publish date
- **Automatic Ordering** - Posts ordered by publish date (descending)
- **Database Index** - Indexed on publish field for performance
- **Absolute URL Method** - Generates canonical URL for each post

### Comment Model

Represents reader comments on posts:

```python
Comment
├── post: ForeignKey         # Link to Post
├── name: CharField          # Commenter name
├── email: EmailField        # Commenter email
├── body: TextField          # Comment text
├── created: DateTimeField   # When comment was posted
├── updated: DateTimeField   # Last update
└── active: BooleanField     # Moderation status
```

**Key Features:**
- **Related Name** - Accessible as `post.comments.all()`
- **Creation Index** - Indexed for efficient querying
- **Moderation Support** - Active/inactive flag for approval
- **Chronological Ordering** - Oldest comments first

---

## Business Logic Layer (Views)

### Function-Based Views

The application uses function-based views for clarity and simplicity:

#### `post_list(request, tag_slug=None)`
- Lists published posts with pagination
- Supports tag-based filtering
- Returns 4 posts per page

#### `Post_detail(request, year, month, day, post)`
- Displays single post with full content
- Shows active comments (with "load more" functionality)
- Displays comment form
- Shows related posts based on shared tags
- Uses date-based URL parameters for SEO

#### `post_share(request, post_id)`
- Email sharing functionality
- Form validation and email sending
- Confirmation message on success

#### `post_comment(request, post_id)`
- POST-only view for submitting comments
- Links comment to specific post
- Returns confirmation template

#### `post_search(request)`
- Full-text search using PostgreSQL
- Trigram similarity ranking
- Searches both title and body fields

---

## Presentation Layer (Templates)

### Template Hierarchy

```
blog/base.html                    # Base template
│
├── blog/post/list.html          # Post listing page
├── blog/post/detail.html        # Individual post page
├── blog/post/home.html          # Homepage
├── blog/post/search.html        # Search results
├── blog/post/share.html         # Email sharing form
├── blog/post/comment.html       # Comment confirmation
└── blog/post/includes/          # Reusable components
    ├── comment_form.html
    ├── search_form.html
    └── footer.html
```

### Template Features

- **Template Inheritance** - DRY principle with `{% extends %}`
- **Template Blocks** - Customizable content areas
- **Template Tags** - Django built-in tags plus custom tags
- **Static Files Loading** - `{% load static %}` for assets
- **URL Reversal** - `{% url %}` tag for dynamic URLs

---

## URL Routing

### URL Structure

```
/                           → home page
/post/                      → post list
/post/?page=2              → paginated post list
/tag/<slug>/               → posts filtered by tag
/post/2026/01/23/my-post/  → individual post detail
/<id>/share/               → share post form
/<id>/comment/             → submit comment
/search/                   → search posts
/feed/                     → RSS feed
```

### URL Design Principles

- **Hierarchical** - Clear parent/child relationships
- **RESTful** - Resource-based naming
- **SEO-Friendly** - Human-readable URLs
- **Date-Based** - Posts include publication date in URL
- **Named URLs** - All URLs have names for reverse resolution

---

## Database Architecture

### Database Support

**Primary: PostgreSQL**
- Full-text search capabilities
- Trigram similarity extension
- Connection pooling
- Advanced indexing

**Fallback: SQLite**
- Development convenience
- Simple setup
- No additional configuration

### Schema Design

```sql
-- Posts Table
blog_post
├── id (PK)
├── title
├── slug (UNIQUE per date)
├── author_id (FK → auth_user)
├── body
├── publish (INDEXED)
├── created
├── updated
└── status

-- Comments Table
blog_comment
├── id (PK)
├── post_id (FK → blog_post)
├── name
├── email
├── body
├── created (INDEXED)
├── updated
└── active

-- Tags (via django-taggit)
taggit_tag
taggit_taggeditem
```

---

## Third-Party Integrations

### django-taggit
- **Purpose**: Tag management
- **Integration**: TaggableManager on Post model
- **Features**: Tag creation, filtering, counting

### python-decouple
- **Purpose**: Configuration management
- **Integration**: Environment variable loading
- **Usage**: Database credentials, email settings

### Markdown
- **Purpose**: Markdown content support
- **Integration**: Optional content formatting
- **Usage**: Rich text in post body

### psycopg
- **Purpose**: PostgreSQL database adapter
- **Version**: psycopg 3.x
- **Features**: Connection pooling, async support

---

## Security Architecture

### Built-In Django Security

- **CSRF Protection** - All forms include CSRF tokens
- **SQL Injection** - Prevented by ORM parameterized queries
- **XSS Prevention** - Automatic template escaping
- **Password Hashing** - PBKDF2 algorithm by default
- **Clickjacking Protection** - X-Frame-Options middleware

### Application-Level Security

- **Email Validation** - Proper email field types
- **Active Flag** - Comment moderation before display
- **POST Requirement** - Comment submission requires POST
- **Published Status** - Only published posts are visible

### Configuration Security

- **Environment Variables** - Secrets stored in `.env` file
- **Secret Key** - Separate from code repository
- **Debug Mode** - Disabled in production
- **Allowed Hosts** - Restricted in production

---

## Performance Optimization

### Database Optimization

- **Indexing** - Strategic indexes on frequently queried fields
- **Custom Managers** - Pre-filtered querysets reduce queries
- **Select Related** - Can be added for author queries
- **Prefetch Related** - Optimizes tag and comment loading

### Application Optimization

- **Pagination** - Limits query results to 4 posts
- **Published Manager** - Filters at database level
- **Comment Limiting** - Progressive loading of comments
- **Static Files** - Separate CSS files for caching

### Template Optimization

- **Server-Side Rendering** - Fast initial page load
- **Template Caching** - Django's template cache loader
- **Minimal JavaScript** - Reduces client-side processing
- **Fragment Caching** - Can be added for expensive queries

---

## Scalability Considerations

### Current Architecture

The application is designed for small to medium traffic:
- Single server deployment
- Session-based state
- File-based static serving

### Scaling Strategies

For higher traffic, consider:
1. **Database**: Connection pooling (already configured), read replicas
2. **Static Files**: CDN for CSS/images/JS
3. **Caching**: Redis or Memcached for query caching
4. **Application**: Multiple Django instances behind load balancer
5. **Sessions**: Database or cache-backed sessions

---

## Design Patterns Used

### Repository Pattern
- Custom managers (`PublishedManager`) abstract data access

### Factory Pattern
- Form classes create validated data objects

### Template Method Pattern
- Base templates define structure, child templates fill in details

### Decorator Pattern
- `@admin.register` for model registration
- `@require_POST` for view restrictions

---

## Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | Django 5.2 |
| **Language** | Python 3.x |
| **Database** | PostgreSQL / SQLite |
| **Template Engine** | Django Templates |
| **Frontend** | HTML5, CSS3 |
| **Email** | SMTP (Gmail) |
| **Tags** | django-taggit |
| **Config** | python-decouple |

---

## Architectural Decisions

### Why Django?
- **Batteries included** - Admin, ORM, auth out of the box
- **Mature ecosystem** - Stable, well-documented, large community
- **Rapid development** - Built-in features reduce development time

### Why Server-Side Rendering?
- **SEO benefits** - Search engines get full HTML
- **Performance** - Fast initial page load
- **Simplicity** - No complex JavaScript build process

### Why PostgreSQL?
- **Full-text search** - Advanced search capabilities
- **Reliability** - ACID compliance, data integrity
- **Features** - Trigram similarity, JSON fields if needed

### Why Minimal JavaScript?
- **Progressive enhancement** - Works without JS
- **Accessibility** - Compatible with screen readers
- **Simplicity** - Easier to maintain and debug

---

[← Back to Documentation Index](README.md)
