# Contributing

Thank you for considering contributing to the Django Blog Project! This document outlines the process and guidelines for contributing.

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Unprofessional conduct

---

## How to Contribute

### Reporting Bugs

Before submitting a bug report:

1. **Check existing issues** - Your bug might already be reported
2. **Test on the latest version** - The bug may already be fixed
3. **Gather information** - Collect details about the issue

**Bug Report Should Include:**

- Clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Django/Python version
- Database being used
- Browser (if frontend issue)
- Screenshots (if applicable)
- Error messages or logs

**Example Bug Report:**

```markdown
**Title:** Post slug not generating correctly with special characters

**Description:**
When creating a post with special characters in the title (e.g., "Python & Django"), 
the slug generation includes the ampersand instead of converting it to "and".

**Steps to Reproduce:**
1. Go to Django admin
2. Create new post with title "Python & Django"
3. Observe auto-generated slug

**Expected:** python-and-django
**Actual:** python-django

**Environment:**
- Django 5.2
- PostgreSQL 15
- Python 3.11
```

### Suggesting Features

Feature suggestions are welcome! Before submitting:

1. **Check if it fits the project scope** - We aim for simplicity
2. **Search existing feature requests**
3. **Consider alternatives**

**Feature Request Should Include:**

- Clear description of the feature
- Why it would be useful
- How it might work
- Potential implementation approach
- Any drawbacks or alternatives considered

---

## Development Workflow

### Setting Up Development Environment

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/django-blog-project.git
   cd django-blog-project
   ```

2. **Set Up Environment**
   ```bash
   cd gold_blog
   python3 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Configure Database**
   ```bash
   # Create .env file
   cp .env.example .env  # If example exists
   # Or create .env with your settings
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### Creating a Branch

Always create a new branch for your work:

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

**Branch Naming Conventions:**

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation changes
- `refactor/what-was-refactored` - Code refactoring
- `test/what-is-tested` - Adding tests

---

## Making Changes

### Code Style Guidelines

#### Python Code

Follow **PEP 8** style guide:

```python
# Good
def get_published_posts(author_id):
    """Return all published posts by the specified author."""
    return Post.published.filter(author_id=author_id)

# Bad
def getPublishedPosts(authorId):
    return Post.published.filter(author_id=authorId)
```

**Key Points:**
- Use 4 spaces for indentation (not tabs)
- Maximum line length: 79 characters
- Use snake_case for functions and variables
- Use PascalCase for class names
- Add docstrings to functions and classes
- Keep imports organized (standard library, third-party, local)

#### HTML/Templates

```django
{# Good #}
{% extends "blog/base.html" %}

{% block content %}
    <div class="post-list">
        {% for post in posts %}
            <article>
                <h2>{{ post.title }}</h2>
            </article>
        {% endfor %}
    </div>
{% endblock %}

{# Bad - inconsistent indentation, no structure #}
{% extends "blog/base.html" %}
{% block content %}
<div class="post-list">
{% for post in posts %}
<article><h2>{{ post.title }}</h2></article>
{% endfor %}
</div>
{% endblock %}
```

#### CSS

```css
/* Good */
.post-list {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.post-list-item {
    margin-bottom: 30px;
    padding: 20px;
    background-color: #f9f9f9;
}

/* Bad - no organization, inconsistent spacing */
.post-list{max-width:800px;margin:0 auto;padding:20px;}
.post-list-item{margin-bottom:30px;padding:20px;background-color:#f9f9f9;}
```

### Django Best Practices

1. **Models**
   - Use verbose names
   - Add helpful `__str__` methods
   - Use appropriate field types
   - Add database indexes where needed

2. **Views**
   - Keep views thin, business logic in models
   - Use class-based views when appropriate
   - Handle errors gracefully
   - Add docstrings

3. **Templates**
   - Use template inheritance
   - Keep logic minimal
   - Use template tags for reusable components

4. **URLs**
   - Use descriptive URL names
   - Follow RESTful conventions
   - Organize by feature/app

### Writing Tests

**Always add tests for new features:**

```python
from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User

class PostModelTest(TestCase):
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
    
    def test_post_str_representation(self):
        """Test that __str__ returns the title."""
        self.assertEqual(str(self.post), 'Test Post')
    
    def test_get_absolute_url(self):
        """Test post URL generation."""
        url = self.post.get_absolute_url()
        self.assertIn('test-post', url)
```

Run tests:

```bash
python manage.py test blog
```

---

## Submitting Changes

### Commit Messages

Write clear, descriptive commit messages:

**Good:**
```
Add category field to Post model

- Add Category model with name and slug
- Add foreign key to Post model
- Create migration
- Update admin to display category
```

**Bad:**
```
Update stuff
Fixed things
WIP
```

**Format:**
```
Short summary (50 characters or less)

More detailed explanation if necessary. Wrap at 72 characters.
Explain the problem that this commit solves and why you chose
this solution.

- Bullet points are okay
- Reference issues: Fixes #123
```

### Pull Request Process

1. **Update Your Branch**
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Push to Your Fork**
   ```bash
   git push origin your-feature-branch
   ```

3. **Create Pull Request on GitHub**
   - Clear title describing the change
   - Detailed description
   - Link to related issues
   - Screenshots if UI changes

**Pull Request Template:**

```markdown
## Description
Brief description of what this PR does.

## Related Issue
Fixes #123

## Changes Made
- Added feature X
- Updated documentation for Y
- Fixed bug in Z

## Testing
- [ ] Tested locally
- [ ] All tests pass
- [ ] Added new tests for features

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Commented code where necessary
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests pass
```

### Code Review Process

1. **Automated Checks**
   - Tests must pass
   - Code style checks
   - No merge conflicts

2. **Manual Review**
   - Maintainers will review your code
   - Address feedback constructively
   - Make requested changes

3. **Approval and Merge**
   - Once approved, maintainers will merge
   - Your contribution will be credited

---

## Development Guidelines

### What We Look For

✅ **Good Contributions:**
- Solves a real problem
- Follows project conventions
- Includes tests
- Updates documentation
- Small, focused changes
- Clean commit history

❌ **Issues to Avoid:**
- Massive refactoring PRs
- Style-only changes across entire codebase
- Features that don't fit project scope
- Incomplete implementations
- Breaking changes without discussion

### Priority Areas

Contributions are especially welcome in:

1. **Bug Fixes** - Always appreciated
2. **Documentation** - Improvements and clarifications
3. **Tests** - Increasing coverage
4. **Performance** - Optimizations
5. **Accessibility** - A11y improvements
6. **Security** - Security enhancements

---

## Community

### Getting Help

- **GitHub Issues** - For bugs and features
- **Discussions** - For questions and ideas
- **Documentation** - Check docs first

### Recognition

All contributors will be:
- Listed in CONTRIBUTORS.md (if we create one)
- Credited in release notes
- Acknowledged in the project

---

## License

By contributing, you agree that your contributions will be licensed under the same [MIT License](../LICENSE) that covers this project.

---

## Questions?

If you have questions about contributing:
1. Check this document
2. Search existing issues
3. Open a new discussion
4. Ask maintainers

Thank you for contributing to making this project better! 🎉

---

[← Back to Documentation Index](README.md)
