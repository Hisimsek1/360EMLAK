# 360EV - Real Estate SaaS Platform

A real estate listing platform built with Flask, featuring 360-degree virtual tours, user dashboards, and a multi-role access system.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-Private-red.svg)]()

## Features

- Authentication with CSRF protection (Flask-Login)
- User profiles with photo upload, bio, city, and profession fields
- Property listings with image galleries
- 360-degree virtual tour creation and viewing (Pannellum.js)
- Role-based access control (user, agent, admin, super_admin)
- Admin panel for user and listing management
- Thread-safe JSON file database with automatic backups
- Production-ready with Gunicorn and environment-based configuration

## Project Structure

```
360EV/
├── app.py                  # Application factory
├── config.py               # Environment configurations
├── wsgi.py                 # WSGI entry point
├── requirements.txt
├── test_app.py
├── blueprints/
│   ├── main/               # Public pages
│   ├── auth/               # Login, register, logout
│   ├── dashboard/          # User panel and profile
│   ├── property/           # Listings
│   ├── tour/               # 360-degree tour editor
│   └── admin/              # Admin panel
├── core/
│   ├── database.py         # JSON database layer
│   ├── data_manager.py     # Data access layer
│   ├── models.py           # User model
│   └── utils.py            # Helpers
├── static/
│   ├── css/style.css
│   ├── js/editor.js
│   └── uploads/
│       ├── profiles/
│       ├── properties/
│       └── tours/
├── templates/
│   ├── base.html
│   ├── main/
│   ├── auth/
│   ├── dashboard/
│   ├── property/
│   ├── tour/
│   ├── admin/
│   └── errors/
└── data/
    ├── data.json
    └── backups/
```

## Setup

**1. Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment**

Copy `.env.example` to `.env` and set the required values:

```env
FLASK_ENV=development
SECRET_KEY=change-this-in-production
```

**4. Run**

```bash
# Development
python app.py

# Production
gunicorn wsgi:app -b 0.0.0.0:5000 -w 4
```

The app will be available at `http://localhost:5000`.

## Testing

```bash
python -m pytest test_app.py -v

# With coverage
pip install pytest-cov
python -m pytest test_app.py --cov=. --cov-report=html
```

## User Roles

| Role | Description |
|------|-------------|
| `user` | Create listings, edit profile |
| `agent` | Extended listing management |
| `admin` | User management, listing moderation |
| `super_admin` | Full system access |

## Configuration

```python
# Development
DEBUG = True
SESSION_COOKIE_SECURE = False

# Production
DEBUG = False
SESSION_COOKIE_SECURE = True
SECRET_KEY = environ.get('SECRET_KEY')  # required

# File uploads
MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # 16 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
```

## Database

Data is stored in `data/data.json` with the following top-level keys:

```json
{
  "users": [],
  "properties": [],
  "pages": [],
  "settings": {},
  "categories": [],
  "cities": []
}
```

Each property may include a `tour` object with scene data for 360-degree tours. Backups are written automatically to `data/backups/`.

## Security

- CSRF protection on all forms (Flask-WTF)
- Passwords hashed with `pbkdf2:sha256`
- `HttpOnly`, `SameSite` session cookies
- File upload validation (type and size)
- Template auto-escaping (XSS prevention)
- Role-based access decorators

## Roadmap

- [ ] Real-time notifications
- [ ] Advanced search and filters
- [ ] Map integration
- [ ] Email notifications
- [ ] RESTful API
- [ ] Payment integration

## License

Private — all rights reserved.
