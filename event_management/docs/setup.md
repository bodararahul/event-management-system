# Setup Guide

Detailed setup instructions for the Event Management System.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- virtualenv or venv (recommended)
- PostgreSQL (optional, for production)
- Git

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd event_management
```

### 2. Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Django Settings
DJANGO_SECRET_KEY=your-very-secret-key-here-change-in-production
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# CORS
CORS_ALLOW_ALL_ORIGINS=true
```

**For Production (PostgreSQL):**
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=event_management
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Database Setup

**SQLite (Development):**
```bash
python manage.py migrate
```

**PostgreSQL (Production):**
1. Create database:
   ```sql
   CREATE DATABASE event_management;
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### 7. Run Tests

Verify everything is working:

```bash
pytest
```

Or with coverage:

```bash
pytest --cov=apps --cov=common --cov-report=html
```

### 8. Start Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

## Development Workflow

### Running Migrations

When models change:

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Accessing Admin Panel

1. Start server: `python manage.py runserver`
2. Navigate to: `http://localhost:8000/admin/`
3. Login with superuser credentials

### API Documentation

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- JSON Schema: `http://localhost:8000/swagger.json`

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest apps/users/tests/test_views.py
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage
```bash
pytest --cov=apps --cov=common
```

### Run Specific Test
```bash
pytest apps/users/tests/test_views.py::TestLogin::test_login_success
```

## Production Deployment

### 1. Update Settings

Use production settings:

```bash
export DJANGO_SETTINGS_MODULE=config.settings.prod
```

Or set in your environment.

### 2. Security Checklist

- [ ] Change `DJANGO_SECRET_KEY` to a strong random value
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Configure `DJANGO_ALLOWED_HOSTS` properly
- [ ] Use PostgreSQL database
- [ ] Configure CORS properly
- [ ] Set up SSL/HTTPS
- [ ] Configure static files serving
- [ ] Set up logging
- [ ] Configure rate limiting

### 3. Static Files

```bash
python manage.py collectstatic
```

### 4. Database

Ensure PostgreSQL is configured and migrations are applied.

### 5. WSGI Server

Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Troubleshooting

### Import Errors

Ensure you're in the virtual environment and all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Database Errors

Check your database configuration in `.env` and ensure the database exists (for PostgreSQL).

### Migration Errors

If migrations fail:

```bash
python manage.py migrate --run-syncdb
```

### Port Already in Use

If port 8000 is in use:

```bash
python manage.py runserver 8001
```

## Common Issues

### Issue: ModuleNotFoundError

**Solution:** Ensure virtual environment is activated and dependencies are installed.

### Issue: Database locked (SQLite)

**Solution:** Close any other connections to the database or use PostgreSQL.

### Issue: JWT token expired

**Solution:** Use the refresh token endpoint or login again.

## Next Steps

1. Review [API.md](API.md) for API usage
2. Check [README.md](../README.md) for project overview
3. Explore the codebase structure
4. Run tests to understand functionality
5. Start building your frontend integration

## Support

For issues or questions:
1. Check the documentation
2. Review test files for usage examples
3. Open an issue on GitHub

