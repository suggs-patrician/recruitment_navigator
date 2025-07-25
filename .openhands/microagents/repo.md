# Recruitment Navigator Repository

## Purpose
This repository contains a Chinese recruitment information navigation website built with Django and Wagtail CMS. The website serves as a centralized platform for browsing job opportunities across different sectors including government agencies (政府机关), public institutions (事业单位), state-owned enterprises (国企), and banks (银行). Users can search, filter, and browse job postings with support for Chinese language content.

## General Setup
- **Framework**: Django 4.2.23 with Wagtail 7.0.2 CMS
- **Language**: Python 3.12
- **Database**: SQLite (development), configurable for production
- **Frontend**: HTML templates with responsive CSS styling
- **Search**: Wagtail search with database fallback for Chinese text queries
- **Deployment**: Docker-ready with Gunicorn server
- **Environment**: Separate settings for development and production

### Key Dependencies
- Django 4.2.23 - Web framework
- Wagtail 7.0.2 - Content Management System
- wagtail-markdown 0.12.1 - Markdown field support
- django-filter 25.1 - Filtering functionality
- haystack 0.42 - Search backend
- Pillow 11.3.0 - Image processing

## Repository Structure

```
recruitment_navigator/
├── home/                           # Home app - main pages
│   ├── models.py                   # HomePage and AboutPage models
│   ├── templates/home/             # Home page templates
│   ├── management/commands/        # Custom management commands
│   │   └── init_data.py           # Data initialization command
│   └── migrations/                 # Database migrations
├── jobs/                          # Jobs app - core functionality
│   ├── models.py                  # JobPost, JobCategory, Region models
│   ├── templates/jobs/            # Job listing and detail templates
│   ├── admin.py                   # Admin interface configuration
│   └── migrations/                # Database migrations
├── search/                        # Search functionality
│   ├── views.py                   # Search logic with Chinese text support
│   └── templates/search/          # Search result templates
├── recruitment_navigator/         # Main project directory
│   ├── settings/                  # Environment-specific settings
│   │   ├── base.py               # Base configuration
│   │   ├── dev.py                # Development settings
│   │   └── production.py         # Production settings
│   ├── templates/                 # Global templates
│   │   └── base.html             # Base template with navigation
│   ├── static/                    # Static files
│   └── urls.py                    # URL configuration
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker configuration
├── manage.py                      # Django management script
└── db.sqlite3                     # SQLite database (development)
```

### Key Features
- **Multilingual Support**: Full Chinese language support with UTF-8 encoded URLs
- **Content Management**: Wagtail CMS for easy content editing
- **Job Filtering**: Filter by category, region, and tags
- **Search Functionality**: Enhanced search with database fallback for Chinese queries
- **Responsive Design**: Mobile-friendly interface
- **Admin Interface**: Wagtail admin panel for content management
- **Data Management**: Custom management command for initializing sample data

### Models
- **HomePage**: Landing page with recent job listings
- **AboutPage**: About us page with rich text content
- **JobPost**: Individual job postings with categories, regions, and tags
- **JobIndexPage**: Job listing page with filtering capabilities
- **JobCategory**: Job categories (government, institution, state-owned, bank)
- **Region**: Hierarchical location system for job filtering

## CI/CD Configuration
No GitHub Actions workflows are currently configured in this repository. The project includes:
- Docker configuration for containerized deployment
- Separate development and production settings
- Static file collection and database migration in Docker CMD
- Gunicorn WSGI server for production deployment

## Development Notes
- Uses Chinese URL slugs (e.g., `/招聘信息/`, `/关于我们/`)
- CSRF protection configured for development domains
- Search functionality enhanced with database queries for better Chinese text support
- Sample data can be initialized using `python manage.py init_data` command
- Admin access available at `/admin/` (default: admin/admin123)