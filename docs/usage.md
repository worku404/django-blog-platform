# Usage

This guide explains how to use the Django Blog Project to create, manage, and view blog posts.

---

## For Blog Authors

### Creating Your First Blog Post

#### Method 1: Using Django Admin (Recommended)

1. **Access the Admin Panel**
   - Navigate to http://127.0.0.1:8000/admin/
   - Log in with your superuser credentials

2. **Navigate to Posts**
   - Click on "Posts" in the left sidebar
   - Click "Add Post" button (top right)

3. **Fill in Post Details**

   **Title**
   - Enter your post title (e.g., "Getting Started with Django")
   - This appears as the main heading

   **Slug**
   - Auto-populated from title
   - URL-friendly version (e.g., "getting-started-with-django")
   - Edit if needed for cleaner URLs

   **Author**
   - Select the author (yourself)
   - Use the magnifying glass icon to search users

   **Body**
   - Write your post content
   - Supports plain text and Markdown
   - No character limit

   **Status**
   - **Draft** - Save without publishing (default)
   - **Published** - Make visible to readers
   
   **Publish Date/Time**
   - Set when the post should appear published
   - Defaults to current date/time
   - Can be set to future date for scheduling

   **Tags**
   - Add comma-separated tags (e.g., "django, python, web development")
   - Creates new tags automatically
   - Used for categorization and related posts

4. **Save the Post**
   - Click "Save and continue editing" to keep working
   - Click "Save and add another" to create another post
   - Click "Save" to return to post list

#### Method 2: Using Django Shell

For programmatic post creation:

```bash
python manage.py shell
```

```python
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

# Get the author
author = User.objects.get(username='your_username')

# Create a post
post = Post.objects.create(
    title="My First Post",
    slug="my-first-post",
    author=author,
    body="This is the content of my first blog post.",
    status=Post.Status.PUBLISHED,
    publish=timezone.now()
)

# Add tags
post.tags.add("django", "tutorial")

print(f"Created: {post.title}")
```

---

## Managing Posts

### Viewing All Posts

In Django Admin:
1. Go to http://127.0.0.1:8000/admin/
2. Click "Posts"
3. See all posts in table format with:
   - Title
   - Slug
   - Author
   - Publish date
   - Status

### Editing Posts

1. Click on the post title in the admin list
2. Make your changes
3. Click "Save"

**Quick Edit:**
- Click directly on inline-editable fields

### Deleting Posts

⚠️ **Warning: This is permanent!**

1. Select post(s) using checkboxes
2. Choose "Delete selected posts" from action dropdown
3. Click "Go"
4. Confirm deletion

### Filtering Posts

Use the right sidebar filters:
- **By Status** - Draft or Published
- **By Created Date** - When post was created
- **By Publish Date** - When post was/will be published

### Searching Posts

Use the search bar at the top:
- Searches in title and body
- Enter keywords and press Enter

### Sorting Posts

Click column headers to sort by:
- Title
- Slug
- Author
- Publish date
- Status

---

## Working with Tags

### Adding Tags to Posts

**During Post Creation:**
1. Scroll to "Tags" field
2. Type comma-separated tags
3. Press Enter or Tab after each tag

**After Post Creation:**
1. Edit the post
2. Add/remove tags in the Tags field
3. Save

### Tag Best Practices

✅ **Do:**
- Use lowercase tags
- Be consistent (e.g., always "python" not "Python")
- Use specific tags ("django-orm" not just "orm")
- Limit to 3-7 tags per post
- Create a tag naming convention

❌ **Don't:**
- Use symbols or special characters
- Create very long tag names
- Use spaces (use hyphens: "web-dev" not "web dev")
- Tag everything with the same tags

### Viewing Posts by Tag

Users can browse posts by tag:
- URL format: `/tag/django/`
- Shows all posts with that tag
- Pagination applies (4 posts per page)

---

## For Blog Readers

### Viewing Blog Posts

#### Homepage
- Navigate to http://127.0.0.1:8000/
- See homepage with introduction and navigation

#### Post List
- Navigate to http://127.0.0.1:8000/post/
- See all published posts in chronological order
- 4 posts per page with pagination
- Each post shows:
  - Title
  - Author
  - Publication date
  - Excerpt
  - Tags

#### Individual Post
- Click on any post title
- URL format: `/post/2026/01/23/post-slug/`
- See:
  - Full post content
  - Author and date
  - Tags
  - Comments
  - Related posts
  - Share and comment options

### Pagination

Navigate between pages:
- **Next/Previous** buttons at bottom
- **Page numbers** for direct access
- Shows "Page X of Y"

### Reading Related Posts

At the bottom of each post:
- See "Related Posts" section
- Based on shared tags
- Up to 4 related posts shown
- Click to read similar content

---

## Searching for Posts

### Using the Search Feature

1. **Access Search**
   - Navigate to http://127.0.0.1:8000/search/
   - Or use search form (if available in navigation)

2. **Enter Search Terms**
   - Type keywords in search box
   - Press Enter or click "Search"

3. **View Results**
   - Results ranked by relevance
   - Shows matching posts
   - Highlights where terms were found

### Search Tips

✅ **Effective Searches:**
- Use specific keywords
- Try multiple related terms
- Use exact phrases in quotes (if supported)
- Be descriptive

❌ **Less Effective:**
- Single common words ("the", "and")
- Very long queries
- Typos (no auto-correct yet)

### Search Features

The search uses PostgreSQL full-text search:
- **Trigram Similarity** - Finds similar words
- **Weighted Results** - Title matches rank higher
- **Relevance Sorting** - Best matches first

---

## Commenting on Posts

### Leaving a Comment

1. **Navigate to Post**
   - Go to any individual post page

2. **Scroll to Comment Form**
   - Found below the post content
   - Below existing comments

3. **Fill in Details**
   - **Name** - Your name
   - **Email** - Your email (not shown publicly)
   - **Comment** - Your comment text

4. **Submit**
   - Click "Add comment" button
   - See confirmation message

### Comment Moderation

⚠️ **Note:** Comments require approval before appearing publicly.

- Admin must set comment to "active"
- Prevents spam and inappropriate content
- You'll see a confirmation but comment may not appear immediately

### Viewing Comments

- Comments shown in chronological order (oldest first)
- Shows:
  - Commenter name
  - Date posted
  - Comment text
- Initial load shows 3 comments
- "Load more" button to see additional comments

---

## Sharing Posts

### Sharing via Email

1. **Navigate to Post**
   - Go to the post you want to share

2. **Click Share Link**
   - Find "Share via email" link
   - Or navigate to `/post-id/share/`

3. **Fill in Form**
   - **Your Name** - Your name
   - **Your Email** - Your email address
   - **To** - Recipient's email
   - **Comments** - Optional personal message

4. **Send**
   - Click "Send" button
   - Recipient receives email with post link

### Email Format

The recipient receives:
```
Subject: [Your Name] recommends you read [Post Title]

Read [Post Title] at [Post URL]

[Your Name]'s comments: [Your message]
```

---

## RSS Feed Subscription

### Subscribe to Updates

1. **Access Feed**
   - Navigate to http://127.0.0.1:8000/feed/

2. **Subscribe**
   - Copy feed URL
   - Add to your RSS reader (Feedly, Inoreader, etc.)

3. **Receive Updates**
   - Get notified of new posts automatically

### Feed Contents

The RSS feed includes:
- Latest published posts
- Title and description
- Publication date
- Link to full post
- Author information

---

## User Interface Navigation

### Main Navigation

Typical navigation includes:
- **Home** - Homepage
- **Blog** - Post list
- **Search** - Search posts
- **About** - About page (if configured)

### Post Actions

On individual posts:
- **Share** - Email sharing
- **Comment** - Leave a comment
- **Tags** - Click to see related posts

### Pagination Controls

- **← Older** - View older posts
- **Newer →** - View newer posts
- **Page 1, 2, 3...** - Jump to specific page

---

## Content Guidelines

### For Authors

When creating posts:

**Title**
- Clear and descriptive
- 50-70 characters ideal
- Include keywords for SEO

**Content**
- Use paragraphs for readability
- Include headers for structure
- Aim for 300+ words for SEO
- Proofread before publishing

**Tags**
- Use 3-7 relevant tags
- Be consistent with naming
- Think about what readers search for

**Publish Date**
- Use current date for immediate publish
- Set future date to schedule
- Past dates for historical content

---

## Keyboard Shortcuts (Admin)

In Django Admin:

- **Ctrl/Cmd + S** - Save form
- **Tab** - Move to next field
- **Shift + Tab** - Move to previous field
- **Alt + S** - Save and continue editing

---

## Tips for Best Experience

### For Authors

1. **Draft First** - Write in Draft status, proofread, then publish
2. **Use Tags Wisely** - Consistent tagging helps readers find content
3. **Preview** - Check your post on the public site before sharing
4. **Schedule Posts** - Use future publish dates to plan content
5. **Edit Slugs** - Clean URLs are more shareable

### For Readers

1. **Use Tags** - Find related content by clicking tags
2. **Subscribe to Feed** - Never miss a new post
3. **Search** - Find specific topics quickly
4. **Share Posts** - Send interesting posts to friends
5. **Leave Comments** - Engage with authors

---

## Mobile Experience

The blog is fully responsive:
- **Mobile-Friendly** - Optimized for phones and tablets
- **Touch-Friendly** - Large tap targets
- **Fast Loading** - Minimal JavaScript
- **Readable** - Typography optimized for small screens

---

## Accessibility

The blog includes accessibility features:
- **Semantic HTML** - Proper heading hierarchy
- **Alt Text** - Images should include descriptions
- **Keyboard Navigation** - All features accessible via keyboard
- **Screen Reader Friendly** - Proper ARIA labels

---

[← Back to Documentation Index](README.md)
