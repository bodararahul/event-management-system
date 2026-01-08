## Event Management System (EMS)

A production-ready Django REST Framework (DRF) backend API for managing events, user registrations, and authentication.

## 🎯 Features

- **JWT Authentication** - Secure token-based authentication
- **Role-Based Access Control** - Admin, Organizer, and User roles
- **Event Management** - Full CRUD operations for events
- **Registration System** - Users can register for events with capacity validation
- **Soft Delete** - Events are soft-deleted to maintain data integrity
- **API Documentation** - Swagger/OpenAPI documentation
- **Comprehensive Testing** - Unit and integration tests using pytest

## 📁 Project Structure

```
event_management/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── config/
│   ├── settings/
│   │   ├── base.py      # Base settings
│   │   ├── dev.py       # Development settings
│   │   └── prod.py      # Production settings
│   ├── urls.py          # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── users/           # User authentication & management
│   ├── events/          # Event CRUD operations
│   └── registrations/   # Event registration system
│
├── common/              # Shared utilities
│   ├── permissions.py
│   ├── pagination.py
│   ├── responses.py
│   ├── constants.py
│   └── utils.py
│
├── tests/               # Test configuration
│   └── conftest.py
│
└── docs/                # Documentation
    ├── API.md
    └── setup.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd event_management
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run tests**
   ```bash
   pytest
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Database (PostgreSQL for production)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=event_management
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432

CORS_ALLOW_ALL_ORIGINS=true
```

## 📚 API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **JSON Schema**: http://localhost:8000/swagger.json

## 🧪 Testing

The project uses `pytest` for testing. Run tests with:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov=common

# Run specific test file
pytest apps/users/tests/test_views.py

# Run with verbose output
pytest -v
```

## 🔑 User Roles

- **ADMIN**: Full access to all endpoints, can delete events
- **ORGANIZER**: Can create and update events, cannot delete
- **USER**: Can view events and register for them

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/logout/` - Logout (blacklist token)
- `GET /api/auth/profile/` - Get current user profile

### Events
- `GET /api/events/` - List all events (with filtering)
- `GET /api/events/{id}/` - Get event details
- `POST /api/events/` - Create event (Admin/Organizer only)
- `PUT /api/events/{id}/` - Update event (Admin/Organizer only)
- `DELETE /api/events/{id}/` - Delete event (Admin only)
- `POST /api/events/{id}/register/` - Register for event

### Registrations
- `GET /api/registrations/` - Get user's registrations
- `GET /api/admin/registrations/` - Get all registrations (Admin only)

For detailed API documentation, see [docs/API.md](docs/API.md).

## 🛠️ Development

### Code Quality

- Type hints on all functions
- Google-style docstrings
- Service layer pattern for business logic
- Thin views that delegate to services
- Comprehensive error handling

### Running in Development Mode

```bash
python manage.py runserver --settings=config.settings.dev
```

### Running in Production Mode

```bash
python manage.py runserver --settings=config.settings.prod
```

## 📦 Dependencies

- Django 4.2+
- Django REST Framework 3.14+
- djangorestframework-simplejwt
- drf-yasg (API documentation)
- pytest & pytest-django (testing)
- python-dotenv (environment variables)
- psycopg2-binary (PostgreSQL support)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Event Management System - Demo Project

## 📞 Support

For issues and questions, please open an issue on GitHub.

