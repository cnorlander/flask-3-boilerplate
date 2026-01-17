"""
Pytest configuration and fixtures for the Flask boilerplate test suite.
This module provides shared test configuration and reusable fixtures for all tests.
"""

import pytest
import tempfile
import os
from boilerplate.app import app
from boilerplate.db import db
from boilerplate.modules.role.role_model import get_role_by_name, seed_roles_if_required, update_system_roles
from boilerplate.modules.user.user_model import User


@pytest.fixture
def client():
    """
    Creates a test client for the Flask application.
    Sets up an in-memory SQLite database for testing.
    
    Yields:
        FlaskClient: A test client for making requests to the app
    """
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    app.config['DB_SEED'] = False
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        # Seed roles for testing
        seed_roles_if_required()
        update_system_roles()
        
        # Create test users
        admin_role = get_role_by_name("System Admin")
        default_role = get_role_by_name("Default Role")
        
        admin = User("admin@test.com", "Admin", "User", "TestPassword123!", admin_role)
        user = User("user@test.com", "Default", "User", "TestPassword123!", default_role)
        inactive = User("inactive@test.com", "Inactive", "User", "TestPassword123!", default_role, active=False)
        
        db.session.add_all([admin, user, inactive])
        db.session.commit()
        
        yield app.test_client()
        
        db.session.remove()
        db.drop_all()
    
    # Clean up the temporary database file
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def runner(client):
    """
    Creates a CLI test runner for the Flask application.
    
    Yields:
        FlaskCliRunner: A runner for testing CLI commands
    """
    yield app.test_cli_runner()


@pytest.fixture
def authenticated_admin_client(client):
    """
    Creates an authenticated test client logged in as an admin user.
    
    Args:
        client: The test client fixture
        
    Returns:
        FlaskClient: An authenticated test client
    """
    client.post('/login', data={
        'email': 'admin@test.com',
        'password': 'TestPassword123!'
    })
    return client


@pytest.fixture
def admin_user(client):
    """
    Returns the admin user UUID created in the client fixture.
    
    Returns:
        str: The admin user's UUID
    """
    with app.app_context():
        from boilerplate.modules.user.user_model import get_user_by_email
        admin = get_user_by_email('admin@test.com')
        return str(admin.uuid) if admin else None


@pytest.fixture
def default_user(client):
    """
    Returns the default user UUID created in the client fixture.
    
    Returns:
        str: The default user's UUID
    """
    with app.app_context():
        from boilerplate.modules.user.user_model import get_user_by_email
        user = get_user_by_email('user@test.com')
        return str(user.uuid) if user else None


@pytest.fixture
def deactivated_user(client):
    """
    Returns the deactivated user UUID created in the client fixture.
    
    Returns:
        str: The deactivated user's UUID
    """
    with app.app_context():
        from boilerplate.modules.user.user_model import get_user_by_email
        user = get_user_by_email('inactive@test.com')
        return str(user.uuid) if user else None


@pytest.fixture
def authenticated_user_client(client):
    """
    Creates an authenticated test client logged in as a default user.
    
    Args:
        client: The test client fixture
        
    Returns:
        FlaskClient: An authenticated test client
    """
    client.post('/login', data={
        'email': 'user@test.com',
        'password': 'TestPassword123!'
    })
    return client
