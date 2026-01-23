# Django Blog Project

A clean, content‑focused blog built with **Django**. This project delivers a simple, elegant publishing experience with a responsive, readable interface and a template‑driven architecture that is easy to extend.

---

## ✨ Overview

**django-blog-project** is a minimal yet functional blogging website designed for authors who want to publish and manage posts with clarity and ease. The application focuses on a straightforward user experience, fast page loads, and content‑first design.

---

## ✅ Key Features

- **Blog post publishing** with titles, content, and dates  
- **Post listing & detail views** for easy browsing
- **Tagging system** for categorizing posts
- **Comment system** with moderation capabilities
- **Email sharing** functionality
- **Full-text search** with PostgreSQL trigram similarity
- **RSS feeds** for content syndication
- **Responsive layout** optimized for mobile and desktop  
- **Clean UI** using lightweight HTML/CSS  
- **Template‑driven pages** for SEO‑friendly rendering  

---

## 🧱 Tech Stack

- **Backend:** Django 5.2 (Python)  
- **Frontend:** HTML, CSS  
- **Database:** PostgreSQL (with full-text search support)
- **Templates:** Django Template Engine
- **Additional Libraries:** django-taggit, Markdown, psycopg  

---

## 📂 Project Structure (Typical)

```
django-blog-project/
├── blog/                 # App with models, views, urls, templates
├── templates/            # Global templates (if used)
├── static/               # CSS, images, JS
├── manage.py
└── requirements.txt
```

---

## 🚀 Getting Started

### 1) Clone the repository
```bash
git clone https://github.com/worku404/django-blog-project.git
cd django-blog-project
```

### 2) Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Apply migrations
```bash
python manage.py migrate
```

### 5) Run the development server
```bash
python manage.py runserver
```

Open your browser at:  
**http://127.0.0.1:8000/**

---

## 🧪 Optional: Create a Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

Then visit:  
**http://127.0.0.1:8000/admin**

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Getting Started](docs/getting-started.md)** - Quick start guide for new users
- **[Installation Guide](docs/installation.md)** - Detailed setup instructions
- **[Project Structure](docs/project-structure.md)** - Architecture and organization
- **[Features](docs/features.md)** - Complete feature documentation
- **[Configuration](docs/configuration.md)** - Environment variables and settings
- **[Development Guide](docs/development.md)** - Development workflow and testing
- **[API Reference](docs/api-reference.md)** - Models, views, and URL patterns
- **[Deployment Guide](docs/deployment.md)** - Production deployment instructions
- **[Contributing](docs/contributing.md)** - Contribution guidelines
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

**Start here:** [Documentation Index](docs/index.md)

---

## 📝 Customization

You can easily extend the project by:
- Adding categories/tags
- Implementing search or filters
- Enhancing the UI with a CSS framework
- Adding comments or user authentication

---

## 📌 Best Use Cases

- Personal blogging  
- Learning Django basics  
- Portfolio content  
- Simple project updates  

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙌 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](docs/contributing.md) for details on:

- Code of conduct
- Development setup
- Coding standards
- Pull request process
- Issue guidelines

Feel free to fork the repo and submit a pull request.

---

## 📫 Contact

If you have questions or suggestions, open an issue or reach out through GitHub.

---

**Built with Django — simple, clean, and content‑first.**
