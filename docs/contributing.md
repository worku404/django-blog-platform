# Contributing Guidelines

Thank you for considering contributing to the Django Blog Project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards other community members

**Unacceptable behaviors include:**
- Trolling, insulting comments, and personal attacks
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:
1. **Check existing issues** to avoid duplicates
2. **Test with latest version** to see if the bug persists
3. **Gather information** about the bug

When creating a bug report, include:
- **Clear title** describing the issue
- **Detailed description** of the problem
- **Steps to reproduce** the bug
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, Django version)
- **Error messages** and stack traces

**Example Bug Report:**
```markdown
## Bug: Comment form doesn't validate email

### Description
The comment form accepts invalid email addresses like "test@" without validation.

### Steps to Reproduce
1. Navigate to any blog post
2. Click "Add Comment"
3. Enter "test@" in email field
4. Submit form

### Expected Behavior
Form should show validation error for invalid email

### Actual Behavior
Form submits successfully with invalid email

### Environment
- OS: Ubuntu 22.04
- Python: 3.11
- Django: 5.2
- Browser: Chrome 120
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Include:
- **Clear title** describing the enhancement
- **Detailed description** of the proposed feature
- **Use cases** explaining why it would be useful
- **Possible implementation** if you have ideas
- **Examples** from other projects (if applicable)

**Example Enhancement:**
```markdown
## Enhancement: Add post categories

### Description
Add a category system alongside tags for better content organization.

### Use Case
Users want to organize posts into broad categories (Tutorial, News, Review)
while using tags for specific topics.

### Proposed Implementation
- Add Category model with name and slug
- Add ForeignKey to Post model
- Add category filter to post list view
- Update templates to display categories

### Examples
Similar to how WordPress handles categories and tags.
```

### Contributing Code

Areas where contributions are welcome:
- **Bug fixes**
- **New features** (discuss in issue first)
- **Documentation improvements**
- **Test coverage**
- **Performance optimizations**
- **UI/UX enhancements**

## Development Setup

### 1. Fork and Clone

```bash
# Fork repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/django-blog-project.git
cd django-blog-project
```

### 2. Set Up Environment

```bash
cd gold_blog
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 3. Configure Database

```bash
# Create PostgreSQL database
createdb django_blog_dev

# Create .env file
cat > .env << EOF
DB_NAME=django_blog_dev
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432
EMAIL_HOST_USER=test@example.com
EMAIL_HOST_PASSWORD=test
DEFAULT_FROM_EMAIL=test@example.com
EOF
```

### 4. Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) style guide:

- **Indentation:** 4 spaces (no tabs)
- **Line length:** Maximum 100 characters
- **Imports:** Group and order properly
- **Naming:**
  - Classes: `PascalCase`
  - Functions/variables: `snake_case`
  - Constants: `UPPER_CASE`

### Django Best Practices

**Models:**
```python
class Post(models.Model):
    """Blog post model."""
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    
    class Meta:
        ordering = ['-publish']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[...])
```

**Views:**
```python
def post_list(request, tag_slug=None):
    """
    Display paginated list of published posts.
    
    Args:
        request: HTTP request object
        tag_slug: Optional tag slug to filter posts
    
    Returns:
        HttpResponse with rendered template
    """
    post_list = Post.published.all()
    # ... implementation
```

**Templates:**
- Use template inheritance
- Keep logic minimal (move to views/models)
- Use meaningful variable names
- Add comments for complex sections

### Code Formatting

Use **Black** for automatic formatting:

```bash
pip install black
black gold_blog/blog/
```

### Linting

Use **Pylint** for code quality:

```bash
pip install pylint
pylint gold_blog/blog/
```

Aim for a score of 8.0 or higher.

### Type Hints

Use type hints for better code clarity:

```python
from typing import Optional, List
from django.http import HttpRequest, HttpResponse

def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Display single post."""
    ...
```

## Commit Guidelines

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(blog): add post categories"
git commit -m "fix(comments): validate email addresses properly"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(models): add tests for Post model"
git commit -m "refactor(views): simplify post_list query logic"
```

### Commit Best Practices

- **One logical change per commit**
- **Write clear, descriptive messages**
- **Reference issues** when applicable: "fix(blog): resolve #123"
- **Keep commits atomic** and reversible

## Pull Request Process

### Before Submitting

1. **Update your branch:**
```bash
git fetch origin
git rebase origin/main
```

2. **Run tests:**
```bash
python manage.py test
```

3. **Check code style:**
```bash
black --check gold_blog/blog/
pylint gold_blog/blog/
```

4. **Update documentation** if needed

### Creating Pull Request

1. **Push your branch:**
```bash
git push origin feature/your-feature-name
```

2. **Open Pull Request** on GitHub

3. **Fill out PR template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] Added tests
- [ ] Tests pass locally
- [ ] No breaking changes
```

### PR Review Process

1. **Automated checks** must pass (if configured)
2. **Code review** by maintainers
3. **Address feedback** in new commits
4. **Approval** from maintainer
5. **Merge** when approved

### After Merge

1. **Delete your branch:**
```bash
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

2. **Update your fork:**
```bash
git checkout main
git pull upstream main
git push origin main
```

## Issue Guidelines

### Creating Issues

**Use templates** when available:
- Bug Report
- Feature Request
- Documentation Improvement

**Include:**
- Clear, descriptive title
- Detailed description
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Environment details
- Related issues or PRs

### Issue Labels

Common labels:
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested
- `wontfix` - This will not be worked on

## Testing Requirements

### Writing Tests

All new features should include tests:

```python
from django.test import TestCase
from blog.models import Post

class PostModelTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            # ... other fields
        )
    
    def test_post_creation(self):
        """Test post is created correctly."""
        self.assertEqual(self.post.title, 'Test Post')
    
    def test_get_absolute_url(self):
        """Test URL generation."""
        url = self.post.get_absolute_url()
        self.assertIsNotNone(url)
```

### Test Coverage

Aim for:
- **Models:** 100% coverage
- **Views:** 80%+ coverage
- **Forms:** 100% coverage
- **Overall:** 80%+ coverage

## Documentation Requirements

### Code Documentation

- **Docstrings** for all functions, classes, and modules
- **Inline comments** for complex logic
- **Type hints** for function signatures

### User Documentation

Update relevant documentation files:
- `docs/features.md` - For new features
- `docs/api-reference.md` - For API changes
- `docs/configuration.md` - For new settings
- `README.md` - For major changes

## Community

### Getting Help

- **GitHub Discussions** - Ask questions
- **GitHub Issues** - Report bugs
- **Pull Requests** - Discuss code changes

### Recognition

Contributors are recognized in:
- GitHub contributors list
- Project README (for significant contributions)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing:
1. Check existing documentation
2. Search closed issues
3. Open a new issue with the `question` label

---

**Thank you for contributing to Django Blog Project!**

---

[← Back to Documentation Index](index.md)
