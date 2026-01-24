# Getting Started

This quick start guide will help you get up and running with the Django Blog Project in minutes.

## Prerequisites

Ensure you've completed the [Installation Guide](installation.md) before proceeding.

## First Steps After Installation

### 1. Access the Admin Interface

Navigate to the Django admin panel:
```
http://127.0.0.1:8000/admin/
```

Login with the superuser credentials you created during installation.

### 2. Create Your First Blog Post

1. In the admin panel, click on **"Posts"** under the **BLOG** section
2. Click **"Add Post"** button in the top right
3. Fill in the post details:
   - **Title:** Enter a compelling title
   - **Slug:** Will auto-populate based on title (can be edited)
   - **Author:** Select your user account
   - **Body:** Write your post content (supports plain text)
   - **Status:** Choose "Published" to make it visible
   - **Publish date:** Set to current date/time or schedule for later
   - **Tags:** Add relevant tags (e.g., "django", "python", "web-development")
4. Click **"Save"**

### 3. View Your Blog

Visit the blog homepage:
```
http://127.0.0.1:8000/
```

Or go directly to the post list:
```
http://127.0.0.1:8000/post/
```

Click on any post title to view the full post detail page.

## Understanding the URL Structure

The blog uses a clear, SEO-friendly URL pattern:

- **Home Page:** `/`
- **Post List:** `/post/`
- **Post Detail:** `/post/YYYY/MM/DD/post-slug/`
- **Tag Filter:** `/tag/tag-name/`
- **Post Search:** `/search/?query=keyword`
- **RSS Feed:** `/feed/`

### Example URLs

```
http://127.0.0.1:8000/post/2026/01/23/my-first-post/
http://127.0.0.1:8000/tag/django/
http://127.0.0.1:8000/search/?query=python
```

## Basic Features Walkthrough

### Creating and Managing Posts

**Draft vs Published:**
- **Draft:** Only visible in admin, won't appear on the site
- **Published:** Visible to all visitors

**Scheduling Posts:**
Set the publish date to a future time to schedule posts for later publication.

### Adding Tags

Tags help organize and categorize your content:

1. When creating/editing a post, scroll to the **"Tags"** field
2. Type a tag name and press Enter
3. Add multiple tags separated by commas or pressing Enter
4. Existing tags will autocomplete as you type

**Viewing Posts by Tag:**
Click any tag on a post detail page to see all posts with that tag.

### Enabling Comments

Comments are enabled by default on all posts:

1. Visitors can leave comments on the post detail page
2. Comments appear below the post content
3. All comments are active by default (visible immediately)
4. Moderate comments in admin: **Blog → Comments**

**Comment Moderation:**
- Mark a comment as inactive to hide it from the site
- Edit or delete inappropriate comments
- Filter by active/inactive status in the admin

### Sharing Posts via Email

Each post has a "Share" button that allows readers to:
1. Enter their name and email
2. Enter recipient's email
3. Add a personal message
4. Send an email with a link to the post

**Note:** Email sharing requires proper email configuration in your `.env` file.

### Using Search

The search feature uses PostgreSQL's trigram similarity:

1. Navigate to `/search/`
2. Enter keywords related to post titles or content
3. Results are ranked by relevance
4. Search works across both title and body text

## Working with Sample Data

If you loaded the sample data during installation:

```bash
python manage.py loaddata mysite_data.json
```

You'll have pre-populated posts to explore. This is great for:
- Testing features
- Understanding the data structure
- Having content to style during theme development

## Customizing Your Blog

### Changing the Site Name

Edit `gold_blog/foodie/settings.py`:
```python
# Add to settings
SITE_NAME = "My Awesome Blog"
```

### Pagination Settings

Posts are paginated with 4 posts per page by default. To change this, edit `gold_blog/blog/views.py`:

```python
# In the post_list function
paginator = Paginator(post_list, 10)  # Change 4 to desired number
```

### Comment Display Limit

By default, 3 comments are shown initially. Change this in `gold_blog/blog/views.py`:

```python
# In the Post_detail function
comment_limit = int(request.GET.get("climit", 5))  # Change 3 to desired number
```

## Development Workflow

### Making Changes

1. Edit code in your preferred editor
2. Django automatically reloads when files change
3. Refresh your browser to see changes
4. Check terminal for any error messages

### Running Management Commands

Common Django commands you'll use:

```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a new superuser
python manage.py createsuperuser

# Open Django shell for testing
python manage.py shell

# Check for common issues
python manage.py check
```

## Next Steps

Now that you're familiar with the basics:

1. **[Explore Features](features.md)** - Learn about all available features in depth
2. **[Project Structure](project-structure.md)** - Understand the codebase organization
3. **[Development Guide](development.md)** - Set up your development environment
4. **[Configuration](configuration.md)** - Advanced configuration options

## Tips for New Django Users

### Learning Resources

- [Official Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/5.2/intro/tutorial01/)
- [Django Models Reference](https://docs.djangoproject.com/en/5.2/topics/db/models/)
- [Django Templates Guide](https://docs.djangoproject.com/en/5.2/topics/templates/)

### Best Practices

1. **Always use a virtual environment** - Keeps dependencies isolated
2. **Never commit sensitive data** - Use `.env` for secrets
3. **Test in development** - Use `DEBUG=True` only in development
4. **Use migrations** - Always create and apply migrations for model changes
5. **Keep dependencies updated** - Regularly update packages for security

### Common Gotchas

- **Static files not loading?** Run `python manage.py collectstatic` in production
- **Changes not appearing?** Check if DEBUG mode is enabled
- **Database errors?** Ensure migrations are applied
- **Template not found?** Verify `TEMPLATES` settings and app order

## Getting Help

If you get stuck:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review error messages in the terminal carefully
3. Search the [Django documentation](https://docs.djangoproject.com/)
4. Look for similar issues on [GitHub](https://github.com/worku404/django-blog-project/issues)
5. Open a new issue with details about your problem

---

[← Back to Documentation Index](index.md) | [Next: Project Structure →](project-structure.md)
