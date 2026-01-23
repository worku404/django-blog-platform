# Django Blog Project

A clean, content‑focused blog built with **Django**. This project delivers a simple, elegant publishing experience with a responsive, readable interface and a template‑driven architecture that is easy to extend.

---

## ✨ Overview

**django-blog-project** is a minimal yet functional blogging website designed for authors who want to publish and manage posts with clarity and ease. The application focuses on a straightforward user experience, fast page loads, and content‑first design.

---

## ✅ Key Features

- **Blog post publishing** with titles, content, and dates  
- **Post listing & detail views** for easy browsing  
- **Responsive layout** optimized for mobile and desktop  
- **Clean UI** using lightweight HTML/CSS  
- **Template‑driven pages** for SEO‑friendly rendering  

---

## 🧱 Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS  
- **Templates:** Django Template Engine  

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

## 📚 Documentation

**Comprehensive documentation is available in the [`docs/`](docs/) directory.**

### Quick Links

- **[Installation Guide](docs/installation.md)** - Detailed setup instructions
- **[Usage Guide](docs/usage.md)** - How to create and manage posts
- **[Admin Guide](docs/admin-usage.md)** - Using the Django admin interface
- **[Architecture](docs/architecture.md)** - Technical architecture overview
- **[Deployment](docs/deployment.md)** - Production deployment guide
- **[Contributing](docs/contributing.md)** - How to contribute

📖 **[View Complete Documentation Index](docs/README.md)**

---

## 🚀 Quick Start

### 1) Clone the repository
```bash
git clone https://github.com/worku404/django-blog-project.git
cd django-blog-project/gold_blog
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

### 4) Configure environment (create .env file)
```bash
# Create .env file with your database and email settings
# See docs/configuration.md for details
```

### 5) Apply migrations
```bash
python manage.py migrate
```

### 6) Create a superuser
```bash
python manage.py createsuperuser
```

### 7) Run the development server
```bash
python manage.py runserver
```

Open your browser at:  
**http://127.0.0.1:8000/**

Admin panel:  
**http://127.0.0.1:8000/admin**

For detailed setup instructions, see the **[Installation Guide](docs/installation.md)**

---

## 📝 Features

- **Blog Post Management** - Create, edit, and publish posts with rich content
- **Tagging System** - Organize posts with django-taggit tags
- **Comments** - Reader engagement with moderation
- **Search** - Full-text search powered by PostgreSQL
- **Email Sharing** - Share posts via email
- **RSS Feeds** - Subscribe to latest posts
- **Responsive Design** - Mobile-friendly interface
- **Admin Interface** - Comprehensive Django admin panel

For a complete feature list, see **[Features Documentation](docs/features.md)**

---

## 🎨 Customization

This blog is designed to be easily customizable. See the **[Customization Guide](docs/customization.md)** for details on:

- Modifying styles and themes
- Adding new features (categories, rich text editor, etc.)
- Creating custom template tags
- Extending the admin interface
- Performance optimizations

---

## 📌 Best Use Cases

- Personal blogging  
- Learning Django basics  
- Portfolio content  
- Simple project updates  

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙌 Contributing

Contributions are welcome! Please read our **[Contributing Guidelines](docs/contributing.md)** before submitting pull requests.

**How to contribute:**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See the [Contributing Guide](docs/contributing.md) for detailed instructions.

---

## 📫 Support

- **Issues**: [GitHub Issues](https://github.com/worku404/django-blog-project/issues)
- **Documentation**: [docs/](docs/)
- **Discussions**: [GitHub Discussions](https://github.com/worku404/django-blog-project/discussions)

---

**Built with Django — simple, clean, and content‑first.**
