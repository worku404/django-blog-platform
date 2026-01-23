# Admin Usage

This comprehensive guide covers how to use the Django Admin interface to manage your blog.

---

## Accessing the Admin Panel

### Login

1. **Navigate to Admin URL**
   ```
   http://127.0.0.1:8000/admin/
   ```

2. **Enter Credentials**
   - Username: Your superuser username
   - Password: Your superuser password

3. **Click "Log in"**

### Creating Admin Users

#### Superuser (Full Access)

```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username
- Email address (optional)
- Password (hidden as you type)
- Password confirmation

#### Staff User (Limited Access)

Via Django Admin:
1. Navigate to **Authentication and Authorization → Users**
2. Click **Add User**
3. Set username and password
4. Click **Save**
5. On next screen, check:
   - **Staff status** - Allows admin access
   - **Active** - Account is active
6. Assign specific permissions
7. Click **Save**

---

## Admin Dashboard Overview

After logging in, you'll see:

```
Django Administration

AUTHENTICATION AND AUTHORIZATION
├── Groups
└── Users

BLOG
├── Comments
├── Posts
└── Tags

SITES
└── Sites

TAGGIT
├── Tag
└── Tagged Items
```

---

## Managing Blog Posts

### Post List View

Navigate to **Blog → Posts** to see:

**Columns:**
- **Title** - Post title (clickable to edit)
- **Slug** - URL identifier
- **Author** - Post author
- **Publish** - Publication date
- **Status** - Draft or Published

**Controls:**
- **Search bar** - Search by title or content
- **Add Post** button (top right)
- **Action dropdown** - Bulk actions
- **Filters** (right sidebar)

### Creating a New Post

1. **Click "Add Post"** (top right)

2. **Fill in Required Fields:**

   **Title**
   ```
   Example: "Building a Django Blog"
   ```
   
   **Slug** (auto-populated)
   ```
   Example: "building-a-django-blog"
   ```
   
   **Author**
   - Click magnifying glass icon
   - Search and select user
   - Or type user ID directly
   
   **Body**
   ```
   Write your post content here.
   Supports plain text and Markdown.
   No character limit.
   ```

3. **Optional Fields:**

   **Publish Date/Time**
   - Default: Current date/time
   - Click "Today" and "Now" shortcuts
   - Or manually enter date and time
   
   **Status**
   - Draft (default) - Not visible to public
   - Published - Visible on blog
   
   **Tags**
   ```
   django, python, tutorial, web-development
   ```
   - Comma-separated
   - Creates tags automatically
   - Case-sensitive

4. **Save Options:**
   - **Save and add another** - Create another post
   - **Save and continue editing** - Stay on this post
   - **Save** - Return to post list

### Editing Posts

**Quick Edit:**
1. Navigate to post list
2. Click on post title
3. Make changes
4. Click "Save"

**Inline Editing:**
- Some fields support inline editing
- Click directly in the field
- Save automatically

### Bulk Actions

Select multiple posts and perform actions:

**Available Actions:**
- **Delete selected posts** - Permanently remove posts

**How to Use:**
1. Check boxes next to posts
2. Select action from dropdown
3. Click "Go"
4. Confirm action

### Filtering Posts

**Right Sidebar Filters:**

**By Status:**
- All
- Draft
- Published

**By Created Date:**
- Any date
- Today
- Past 7 days
- This month
- This year

**By Publish Date:**
- Any date
- Today
- Past 7 days
- This month
- This year

**Combining Filters:**
- Click multiple filters to narrow results
- "Clear all filters" link to reset

### Searching Posts

**Search Box (Top of Page):**

Searches in:
- Post title
- Post body

**Tips:**
- Enter keywords
- Press Enter to search
- Case-insensitive
- Partial matches work

### Sorting Posts

Click column headers to sort:
- **Title** - Alphabetical
- **Slug** - Alphabetical
- **Author** - By username
- **Publish** - By date
- **Status** - Draft/Published

Click again to reverse order.

---

## Managing Comments

### Comment List View

Navigate to **Blog → Comments** to see:

**Columns:**
- **Name** - Commenter name
- **Email** - Commenter email
- **Post** - Associated post (clickable)
- **Created** - When comment was posted
- **Active** - Moderation status

### Comment Moderation

**Approving Comments:**
1. Click on comment to open
2. Check **Active** checkbox
3. Click "Save"

**Bulk Approval:**
1. Select multiple comments
2. Choose "Activate comments" action (if configured)
3. Click "Go"

### Comment Details

Click on a comment to see:
- **Post** - Which post it's on
- **Name** - Commenter name
- **Email** - Contact email
- **Body** - Comment text
- **Created** - Timestamp
- **Updated** - Last modification
- **Active** - Visibility status

### Deleting Comments

**Single Comment:**
1. Open comment
2. Click "Delete" (bottom left)
3. Confirm deletion

**Multiple Comments:**
1. Select comments via checkboxes
2. Choose "Delete selected comments"
3. Click "Go"
4. Confirm

### Filtering Comments

**By Active Status:**
- All
- Active (approved)
- Inactive (pending)

**By Created Date:**
- Any date
- Today
- Past 7 days
- This month

**By Updated Date:**
- Similar to created date

### Searching Comments

Search in:
- Commenter name
- Email address
- Comment body

---

## Managing Tags

### Viewing Tags

Navigate to **Taggit → Tags** to see:
- **Name** - Tag name
- **Slug** - URL-friendly version

### Creating Tags Manually

Tags are usually created automatically when added to posts, but you can create them manually:

1. Click "Add Tag"
2. **Name** - Tag name (e.g., "django")
3. **Slug** - Auto-populated (e.g., "django")
4. Click "Save"

### Editing Tags

**Rename a Tag:**
1. Click on tag name
2. Edit name
3. Click "Save"
4. All posts with this tag are updated

**Merge Tags:**
1. Find duplicate tags
2. Edit one to match the other
3. Delete the duplicate
4. Posts reassigned to remaining tag

### Tag Best Practices

**In Admin:**
- Review tags periodically
- Remove unused tags
- Merge similar tags (e.g., "Django" and "django")
- Keep tag names consistent

---

## Managing Users

Navigate to **Authentication and Authorization → Users**

### User List

Shows:
- **Username**
- **Email address**
- **First name**
- **Last name**
- **Staff status**

### Creating Users

See "Creating Admin Users" section above.

### User Permissions

**Permission Levels:**

**Superuser:**
- Full access to everything
- Can't be restricted

**Staff with Permissions:**
- Grant specific permissions
- **Add/Change/Delete** for each model
- **View** permission

**Permission Examples:**
```
blog | post | Can add post
blog | post | Can change post
blog | post | Can delete post
blog | post | Can view post
blog | comment | Can change comment
```

**How to Set Permissions:**
1. Edit user
2. Scroll to **User permissions**
3. Select permissions from "Available"
4. Click arrow to move to "Chosen"
5. Save

### User Groups

**Creating Groups:**
1. Navigate to **Groups**
2. Click "Add Group"
3. **Name** - Group name (e.g., "Editors")
4. **Permissions** - Select relevant permissions
5. Save

**Assigning Users to Groups:**
1. Edit user
2. Scroll to **Groups**
3. Select group
4. Save

**Benefits:**
- Easier permission management
- Consistent access levels
- Scalable for multiple users

---

## Advanced Admin Features

### Date Hierarchy

For posts, a date hierarchy appears at the top:
```
2026 › January › 23
```

Click any level to filter:
- **2026** - All posts in 2026
- **January** - All posts in January 2026
- **23** - All posts on January 23, 2026

### Prepopulated Fields

**Slug Field:**
- Automatically filled from title
- Updates as you type title
- Can be manually edited
- Only works when creating new posts

### Raw ID Fields

**Author Field:**
- Instead of dropdown, shows lookup icon
- Click magnifying glass to search users
- Better performance with many users
- Shows user ID

### Change History

**View Changes:**
1. Open any post/comment
2. Click "History" (top right)
3. See list of all changes:
   - Who made the change
   - When it was changed
   - What action was taken

**History Details:**
- Creation timestamp
- All edits
- Who edited
- Cannot be modified

---

## Customization Tips

### List Display Customization

The list views show the most important fields. These are configured in `admin.py`:

```python
list_display = ['title', 'slug', 'author', 'publish', 'status']
```

### Search Fields

Configured search fields:

```python
search_fields = ['title', 'body']  # For posts
search_fields = ['name', 'email', 'body']  # For comments
```

### List Filters

Sidebar filters configured:

```python
list_filter = ['status', 'created', 'publish']  # For posts
list_filter = ['active', 'created', 'updated']  # For comments
```

---

## Admin Workflow Best Practices

### Content Creation Workflow

1. **Draft First**
   - Create post with Draft status
   - Write and revise content
   - Add tags

2. **Review**
   - Preview on public site
   - Check formatting
   - Proofread

3. **Publish**
   - Change status to Published
   - Set publish date
   - Save

### Comment Moderation Workflow

1. **Regular Checks**
   - Visit Comments section daily
   - Filter by "Inactive"

2. **Review Comments**
   - Read each comment
   - Check for spam/inappropriate content

3. **Approve or Delete**
   - Set Active=True for good comments
   - Delete spam/inappropriate

4. **Respond (Optional)**
   - Could add admin response feature
   - Or email commenter

### Tag Management Workflow

**Monthly Review:**
1. Go to Tags list
2. Look for:
   - Duplicates (django/Django)
   - Typos
   - Unused tags
3. Merge or delete as needed

---

## Security Best Practices

### Password Management

**Strong Passwords:**
- Minimum 8 characters
- Mix of letters, numbers, symbols
- Avoid common words
- Use password manager

**Change Passwords:**
1. Top right: Click username
2. "Change password"
3. Enter old and new passwords
4. Save

### Session Management

**Logout:**
- Always log out when done
- Click "Log out" (top right)

**Session Timeout:**
- Sessions expire after inactivity
- You'll need to log in again

### Permission Discipline

**Principle of Least Privilege:**
- Give users only necessary permissions
- Regular users shouldn't be superusers
- Review permissions periodically

---

## Troubleshooting

### Can't Save Post

**Check:**
- All required fields filled
- Slug is unique for that date
- Author is selected

### Tags Not Working

**Check:**
- Tags are comma-separated
- No special characters
- django-taggit is installed

### Search Not Finding Posts

**Check:**
- Searching in right fields (title, body)
- Spelling is correct
- Post is actually published

### Performance Issues

**If Admin is Slow:**
- Too many posts? Use filters
- Database needs optimization?
- Check server resources

---

## Mobile Admin Access

The Django admin is responsive:
- Works on tablets
- Limited on phones
- Best experience on desktop
- Touch-friendly interfaces

---

[← Back to Documentation Index](README.md)
