# Gold Blog

A Django blog with authentication, tagging, search, email sharing, likes,comments and an integrated AI chat assistant.

## Overview
Gold Blog is a production-style Django app with a clean UI, Markdown posts, and a sidebar AI assistant. Most content pages require authentication.

## Key Features
- User auth: register, login, logout, password reset, change password
- AI chat assistant in the sidebar and a full page, session-based history, Gemini API backend
- Post publishing with drafts, tags, and related-post recommendations
- Markdown rendering for post bodies
- Commenting system for posts (user-linked, moderation-ready)
- Search using PostgreSQL trigram similarity
- Share posts by email (SMTP)
- Like and unlike posts with AJAX
- RSS feed for latest posts
- Sidebar widgets for latest posts and most-commented posts
- Pagination and tag filtering
- Optional Google OAuth login

## Tech Stack
- Django 6.x, Python 3
- PostgreSQL recommended (SQLite supported for local dev)
- django-taggit, social-auth-app-django, python-decouple, python-dotenv
- Google Gemini API via requests, Markdown for rendering AI responses
- WhiteNoise for static files, Gunicorn for deployment
- Commenting system for posts (user‑linked comments, moderation ready)

## Project Structure
```
Gold_blog/
  gold_blog/
    account/
    blog/
    foodie/
    staticfiles/
    manage.py
    requirements.txt
```

## Local Setup
1. `cd gold_blog`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate` or `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. Create `gold_blog/foodie/.env` or export environment variables
6. `python manage.py migrate`
7. `python manage.py runserver`

Open `http://127.0.0.1:8000/`.

## Environment Variables
| Variable | Required | Purpose |
| --- | --- | --- |
| SECRET_KEY | yes | Django secret key |
| DEBUG | no | True or False |
| ALLOWED_HOSTS | no | Comma-separated hosts |
| DATABASE_URL | no | Postgres connection string |
| EMAIL_HOST_USER | for email | SMTP username |
| EMAIL_HOST_PASSWORD | for email | SMTP password (Gmail App Password if using Gmail) |
| DEFAULT_FROM_EMAIL | no | From header for outgoing mail |
| GEMINI_API_KEY_1 | for AI | Gemini API key |
| GEMINI_API_KEY_2 | optional | Additional Gemini API key |
| GEMINI_API_KEY_3 | optional | Additional Gemini API key |
| GEMINI_API_KEY_4 | optional | Additional Gemini API key |
| GOOGLE_OAUTH2_KEY | optional | Google OAuth client ID |
| GOOGLE_OAUTH2_SECRET | optional | Google OAuth client secret |
| DJANGO_SUPERUSER_USERNAME | optional | For non-interactive superuser creation |
| DJANGO_SUPERUSER_EMAIL | optional | For non-interactive superuser creation |
| DJANGO_SUPERUSER_PASSWORD | optional | For non-interactive superuser creation |

## Admin User
- Interactive: `python manage.py createsuperuser`
- Non-interactive: set `DJANGO_SUPERUSER_*` and run `python manage.py create_superuser`

## Notes
- The AI chat uses session history and stores recent turns in the user session.
- Search uses `TrigramSimilarity` and requires PostgreSQL with the `pg_trgm` extension.
- Comments are supported; the UI can be toggled in `gold_blog/blog/templates/blog/post/detail.html` if needed.

## License
MIT License. See `LICENSE`.

## Contributing
Contributions are welcome. Open an issue or submit a pull request.
