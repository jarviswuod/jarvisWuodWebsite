# Jarvis Web Portfolio Website

A modern portfolio website built with Django and TailwindCSS to showcase web development skills, share technical blogs, and post web developer job opportunities for the community.

## 🚀 Features

- **Portfolio Showcase**: Display your projects, skills, and experience
- **Blog System**: Share technical articles and insights with integrated CKEditor
- **Job Board**: Post and share web developer job opportunities
- **Responsive Design**: Mobile-first design using TailwindCSS
- **Admin Interface**: Easy content management through Django admin
- **SEO Optimized**: Built-in sitemap generation for better search visibility
- **Security**: Admin honeypot protection against malicious attacks

## 🛠️ Tech Stack

- **Backend**: Django 5.0.14
- **Frontend**: TailwindCSS + JavaScript
- **Database**: SQLite (Development)
- **Editor**: CKEditor 5 for rich text editing
- **Email**: SendGrid integration for contact forms
- **Environment**: Python virtual environment with django-environ

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** (Latest stable version recommended)
- **Git** for version control
- **Code Editor** (VS Code, PyCharm, etc.)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd jarvis-portfolio-website
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite is default for development)
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=your-email@example.com

# Security
ADMIN_HONEYPOT_EMAIL_ADMINS=True
```

### 5. Database Setup

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### 6. Static Files Setup

```bash
# Collect static files
python manage.py collectstatic --noinput
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view your website!

## 📁 Project Structure

```
jarvis-portfolio-website/
├── manage.py
├── requirements.txt
├── .env
├── db.sqlite3
├── logs/
│   └── django.log
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
├── templates/
└── your_project/
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## 🔧 Development Workflow

### Running the Development Server

```bash
# Always activate your virtual environment first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Then run the server
python manage.py runserver
```

### Making Database Changes

```bash
# After modifying models
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Managing Static Files

```bash
# Collect static files after changes
python manage.py collectstatic
```

### Accessing Admin Interface

1. Navigate to `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials
3. Manage your portfolio content, blog posts, and job listings

### Admin Honeypot Security

- The real admin is at `/admin/`
- Fake admin honeypot is at `/admin-honeypot/` (catches malicious attempts)
- Check logs for security alerts

## 📝 Key Components

### CKEditor Integration

- Rich text editor for blog posts and content
- Configured for optimal user experience
- Supports images, links, and formatted text

### TailwindCSS Styling

- Utility-first CSS framework
- Responsive design out of the box
- Easy customization and theming

### SEO Features

- Automatic sitemap generation
- Meta tags optimization
- Clean URL structure

### Logging

- All logs stored in `logs/django.log`
- Includes error tracking and admin activity
- Configurable log levels

## 🎨 Customization

### Adding New Content Types

1. Create models in your apps
2. Run migrations
3. Register in admin.py
4. Create templates
5. Update URLs

### Styling Changes

- Modify TailwindCSS classes in templates
- Add custom CSS in static files
- Use Django template inheritance

### JavaScript Enhancements

- Add custom JS files to `static/js/`
- Include in templates using `{% load static %}`
- Follow PEP 8 conventions for Python code

## 🐛 Troubleshooting

### Common Issues

**Virtual Environment Not Activated**

```bash
# Make sure you see (venv) in your terminal
source venv/bin/activate
```

**Missing Dependencies**

```bash
pip install -r requirements.txt
```

**Database Issues**

```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**Static Files Not Loading**

```bash
python manage.py collectstatic --clear
```

**Environment Variables Not Loading**

- Check `.env` file exists in project root
- Verify syntax (no spaces around =)
- Restart development server

### Debug Mode

- Keep `DEBUG=True` in development
- Check `logs/django.log` for detailed errors
- Use Django's error pages for debugging

## 📚 Next Steps

### Planned Features

- **Background Tasks**: Celery integration for email processing
- **User Authentication**: Registration and login system
- **API Endpoints**: REST API for mobile app integration
- **Testing Suite**: Comprehensive test coverage
- **Frontend Framework**: Potential React.js integration

### Performance Optimization

- Database query optimization
- Image compression
- Caching implementation
- CDN integration for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Follow PEP 8 coding standards
5. Test your changes
6. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review Django documentation
3. Check the logs in `logs/django.log`
4. Open an issue in the repository

## 🚀 Deployment

This README focuses on development setup. For production deployment with Nginx and Gunicorn, refer to the deployment documentation (coming soon).

---

**Happy Coding! 🎉**

Built with ❤️ using Django and TailwindCSS
