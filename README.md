# Flask 3 Boilerplate

A modern, feature-rich Flask web application boilerplate designed as a jumping-off point for future projects. This project includes a complete user and role management system with authentication, permission handling, and containerized deployment.

## Features

### Authentication & Security
- [X] User authentication with Flask-Login and Bcrypt password hashing
- [X] Password reset functionality with time-limited reset codes
- [X] Session management with secure cookie handling
- [X] User deactivation/activation with role-based permissions
- [X] Anonymous user support for unauthenticated access

### User & Role Management
- [X] Complete user management system with create, read, update, and delete operations
- [X] User profile pages with editable information
- [X] User deactivation and reactivation with permission controls
- [X] Flexible role-based access control (RBAC) system
- [X] Role creation, editing, and deletion with permission assignment
- [X] Action-based permission system for granular access control
- [X] Permission dependency tracking (prevents disabling required permissions)
- [X] System roles and hidden roles for administrative purposes

### Database & ORM
- [X] Flask-SQLAlchemy ORM for database operations
- [X] SQLite database for easy portability
- [X] UUID-based user and role identifiers
- [X] Comprehensive database schema with relationships

### Frontend & UI
- [X] Bootstrap 5 integration for responsive design
- [X] Fancy login page
- [X] Modal-based dialogs for role management
- [X] Dismissible Bootstrap alerts for flash messages
- [X] User-friendly form validation with real-time feedback
- [X] Toggle-able edit modes for profile pages
- [X] Icon integration with Font Awesome
- [X] Responsive navigation with collapsible sidebar

### Development & Deployment
- [X] Docker and Docker Compose configuration for containerized deployment
- [X] Gunicorn WSGI HTTP server for production
- [X] NGINX reverse proxy and static file serving
- [X] Automatic self-signed SSL certificate generation
- [X] Structured logging system


## Prerequisites
- Docker and Docker Compose (recommended)
- Python 3.8+ (if running locally without Docker)
- pip and virtualenv (for local development)

## Quick Start with Docker

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd flask-2-boilerplate
   ```

2. **Start the application:**
   ```bash
   docker-compose up
   ```

   > **Note:** Some workers may fail to start initially while database initialization is completing. This is normal behavior. Simply wait a few moments as the application establishes the database, and the workers will come online automatically.

3. **Access the application:**
   - Open your browser and navigate to `https://localhost`
   - Accept the self-signed certificate warning
   - Login with the default credentials:
     - Email: `admin@default.com`
     - Password: `iloveflask!`

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

## Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd flask-2-boilerplate
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python -m boilerplate.app
   ```

5. **Access the application:**
   - Navigate to `http://localhost:5000`
   - Login with the default credentials:
     - Email: `admin@default.com`
     - Password: `iloveflask!`

## Configuration

Edit `boilerplate/config.py` to customize:
- Password requirements (minimum/maximum length, character types)
- Password reset code validity duration
- Database settings
- Debug mode
- Session configuration

## Default Users

The application seeds three default users if the database is empty:

| Email | Password | Role | Status |
|-------|----------|------|--------|
| admin@default.com | iloveflask! | System Admin | Active |
| default@default.com | iloveflask! | Default Role | Active |
| deactive@default.com | iloveflask! | Default Role | Inactive |

> ⚠️ **Important:** Change these credentials in production!

## Default Roles
- **System Admin:** Full system access
- **Anonymous:** For unauthenticated users
- **Default Role:** Basic user permissions

## Project Structure

```
flask-3-boilerplate/
├── boilerplate/
│   ├── modules/
│   │   ├── login/           # Login authentication
│   │   ├── role/            # Role management system
│   │   └── user/            # User management system
│   ├── static/
│   │   ├── css/             # Stylesheets
│   │   └── js/              # JavaScript files (fully commented)
│   ├── templates/
│   │   ├── components/      # Reusable template components
│   │   ├── login/           # Login templates
│   │   ├── role/            # Role management templates
│   │   └── user/            # User management templates
│   ├── utils/               # Utility functions
│   ├── logs/                # Application logs
│   ├── app.py              # Flask application initialization
│   ├── config.py           # Configuration settings
│   ├── db.py               # Database initialization
│   └── errors.py           # Error handling
├── tests/                   # Test suite (63 tests with full coverage)
│   ├── conftest.py         # Pytest configuration and shared fixtures
│   ├── test_*.py           # Individual test modules
│   └── README.md           # Testing documentation
├── nginx/                   # NGINX configuration
│   ├── nginx.conf          # NGINX server configuration
│   └── ssl/                # SSL certificate generation and storage
├── scripts/                 # Utility scripts
│   ├── run_docker_tests.sh  # Test runner with visual countdown
│   └── rename_project.sh    # Project rename utility
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
└── entrypoint.sh           # Container entrypoint script
```

## Future Enhancement Suggestions

While this project has solid foundations, consider these enhancements for production use:

- **Authentication:** Integrate SSO with Python-SAML or OpenID Connect
- **Database:** Migrate from SQLite to PostgreSQL, MySQL, or other production database
- **Monitoring:** Integrate application monitoring and error tracking
- **Email:** Implement actual email sending for password reset functionality
- **Audit Logging:** Track user actions and changes for compliance
- **Two-Factor Authentication:** Add 2FA for enhanced security

## Testing

The project includes a comprehensive test suite with **63 passing tests** covering:

- ✅ Authentication & login/logout
- ✅ User management (CRUD operations, profiles, deactivation)
- ✅ Roles & permissions system
- ✅ Error handling and HTTP status codes
- ✅ Core app functionality

### Quick Test Run

```bash
./scripts/run_docker_tests.sh
```

This will:
- Start Docker containers automatically
- Show a visual countdown while the app starts
- Run all 63 tests
- Clean up containers after completion

For more information on testing, see [tests/README.md](tests/README.md) which includes:
- Running specific tests
- Coverage reports
- Adding new tests
- Troubleshooting

## License

See LICENSE.md for license information.

