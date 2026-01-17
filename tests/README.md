# Test Suite

Comprehensive test suite for the Flask 2 Boilerplate application using pytest.

## Overview

**63 Passing Tests** covering:
- **Authentication**: Login, logout, password reset, and session management (13 tests)
- **Core Functionality**: App setup, database, roles, and password validation (21 tests)
- **User Management**: User CRUD operations, profile management, deactivation/activation (15 tests)
- **Roles & Permissions**: Role management, permission assignment, and access control (9 tests)
- **Error Handling**: Error pages and HTTP status codes (6 tests)

## Quick Start

### Run Tests with Docker (Recommended)

```bash
./scripts/run_docker_tests.sh
```

This script:
- ✅ Starts Docker containers automatically
- ✅ Shows a visual countdown while app starts
- ✅ Runs all 63 tests
- ✅ Cleans up containers after completion

### Run Tests Locally

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage Report

```bash
pytest --cov=boilerplate tests/ --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_authentication.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_user_management.py::TestUserCreation -v
```

### Run Specific Test

```bash
pytest tests/test_authentication.py::TestLoginFunctionality::test_admin_login_with_valid_credentials -v
```

## Test Structure

```
tests/
├── conftest.py                 # Pytest fixtures and configuration
├── test_core.py               # Core app, database, and basic functionality (21 tests)
├── test_authentication.py      # Login, logout, password reset (13 tests)
├── test_user_management.py    # User CRUD, profiles, deactivation (15 tests)
├── test_roles_permissions.py  # Role management and permissions (9 tests)
├── test_error_handling.py     # Error pages and HTTP status codes (6 tests)
└── README.md                  # This file
```

## Test Fixtures

### Database & Client

**`client`** - Test client with isolated SQLite database
- Automatically creates test users: admin, user, inactive
- Automatically seeds system roles
- Cleans up after each test

### User Fixtures

**`admin_user`** - Returns admin user UUID
- Email: `admin@test.com`
- Role: System Admin
- Status: Active

**`default_user`** - Returns regular user UUID
- Email: `user@test.com`
- Role: Default Role
- Status: Active

**`deactivated_user`** - Returns inactive user UUID
- Email: `inactive@test.com`
- Role: Default Role
- Status: Inactive

### Authenticated Clients

**`authenticated_admin_client`** - Logged in as admin
**`authenticated_user_client`** - Logged in as regular user

## Test Credentials

All test users share the same password:

```
Email: {varies}
Password: TestPassword123!
```

Default test users created in fixtures:
- `admin@test.com` (System Admin)
- `user@test.com` (Default Role)
- `inactive@test.com` (Inactive user)

## Example Tests

### Login Test
```python
def test_admin_login_with_valid_credentials(client):
    """Test admin login with correct credentials."""
    response = client.post('/login', data={
        'email': 'admin@test.com',
        'password': 'TestPassword123!'
    }, follow_redirects=True)
    assert response.status_code == 200
```

### User Management Test
```python
def test_admin_can_view_user_profile(authenticated_admin_client, admin_user):
    """Test that admin can view a user profile."""
    response = authenticated_admin_client.get(f'/users/{admin_user}')
    assert response.status_code == 200
```

### Permission Test
```python
def test_admin_can_create_users(client):
    """Test that admin has permission to create users."""
    with app.app_context():
        admin = get_user_by_email('admin@test.com')
        assert admin.can('create_or_edit_user')
```

## Test Results

Recent test run:
- ✅ 63 tests PASSED
- ⏱️ ~105 seconds total runtime
- 📊 No failures
- ⚠️ 2 minor deprecation warnings (datetime module)

## Docker Test Runner

The script `./scripts/run_docker_tests.sh` provides an easy way to run tests in Docker:

### Features

✨ **Visual Countdown** - Shows progress while container starts (15 seconds)
🐳 **Docker Integration** - Automatically starts/stops containers
📊 **Multiple Options**:
- `-v` - Verbose output
- `-c` - Coverage report
- `--build` - Build containers first
- `--help` - Show all options

### Usage

```bash
# Run all tests
./scripts/run_docker_tests.sh

# Run with coverage
./scripts/run_docker_tests.sh -c

# Run with verbose output
./scripts/run_docker_tests.sh -v

# Build and run
./scripts/run_docker_tests.sh --build

# Show help
./scripts/run_docker_tests.sh --help
```

## Test Best Practices

1. **Use Fixtures**: Leverage conftest.py for setup/teardown
2. **Descriptive Names**: Clear test function names
3. **Docstrings**: Explain what each test verifies
4. **Isolation**: Tests should be independent
5. **App Context**: Use `with app.app_context():` for database queries
6. **Form Data**: Use correct field names (`first-name`, `last-name`, `role-id`, `password-confirm`)

## Common Issues & Solutions

### Issue: Tests Return 400 Bad Request

**Solution**: Form fields must use hyphens, not underscores:
- ✅ `first-name` (correct)
- ❌ `first_name` (wrong)
- ✅ `last-name` (correct)
- ✅ `role-id` (correct)
- ✅ `password-confirm` (correct)

### Issue: DetachedInstanceError

**Solution**: Fetch fresh objects within app context:
```python
with app.app_context():
    user = get_user_by_email('user@test.com')
    assert user.active is True
```

### Issue: Tests Timing Out

**Solution**: Script includes 15-second startup countdown. If tests still hang, check Docker:
```bash
docker compose ps
docker compose logs flask
```

## Adding New Tests

1. Choose appropriate test file or create new `test_*.py`
2. Use existing fixtures from conftest.py
3. Follow naming convention: `test_<feature>` or `TestClassName`
4. Use `with app.app_context():` for database operations
5. Run: `pytest tests/test_yourfile.py -v`

Example:

```python
def test_new_feature(authenticated_admin_client):
    """Test that new feature works correctly."""
    response = authenticated_admin_client.get('/new-feature')
    assert response.status_code == 200
    assert b'expected content' in response.data
```

## Advanced Testing

### Run Only Failed Tests

```bash
pytest --lf
```

### Run Failed Tests First

```bash
pytest --ff
```

### Stop on First Failure

```bash
pytest -x
```

### Detailed Failure Information

```bash
pytest -vv --tb=long
```

### Print Debug Output

```bash
pytest -s
```

## Maintenance

- Keep test count above 60
- Maintain pass rate at 100%
- Review warnings in test output
- Update README when tests change
- Run full suite before committing

## Contact & Support

For test-related issues, check:
1. Test output for error messages
2. This README troubleshooting section
3. Docker logs: `docker compose logs flask`
4. Flask app logs: Check `boilerplate/logs/`
