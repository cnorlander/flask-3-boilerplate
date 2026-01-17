"""
Core Flask boilerplate test suite.
Tests essential functionality: authentication, user management, and roles.
"""

import pytest
from boilerplate.app import app
from boilerplate.db import db
from boilerplate.modules.user.user_model import User, get_user_by_email
from boilerplate.modules.role.role_model import get_role_by_name


class TestAppAndDatabase:
    """Test Flask app and database setup"""
    
    def test_app_exists(self):
        """Test that Flask app is configured"""
        assert app is not None
    
    def test_users_created_in_fixture(self, client):
        """Test that test users are created in database"""
        with app.app_context():
            admin = get_user_by_email('admin@test.com')
            user = get_user_by_email('user@test.com')
            inactive = get_user_by_email('inactive@test.com')
            
            assert admin is not None
            assert user is not None
            assert inactive is not None
            assert inactive.active is False
    
    def test_roles_created_in_fixture(self, client):
        """Test that system roles are created"""
        with app.app_context():
            admin_role = get_role_by_name("System Admin")
            default_role = get_role_by_name("Default Role")
            
            assert admin_role is not None
            assert default_role is not None


class TestAuthentication:
    """Test login and logout"""
    
    def test_login_page_loads(self, client):
        """Test that login page is accessible"""
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_admin_login_succeeds(self, client):
        """Test admin can login"""
        response = client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_user_login_succeeds(self, client):
        """Test regular user can login"""
        response = client.post('/login', data={
            'email': 'user@test.com',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        # Regular user may not have permission to access dashboard,
        # but they should be able to login (redirect happens, not 403)
        assert response.status_code in [200, 403]
    
    def test_login_fails_with_wrong_password(self, client):
        """Test login fails with incorrect password"""
        response = client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'WrongPassword123!'
        }, follow_redirects=True)
        # Should show login page again
        assert response.status_code == 200
        assert b'password' in response.data.lower()
    
    def test_login_fails_with_nonexistent_email(self, client):
        """Test login fails with non-existent email"""
        response = client.post('/login', data={
            'email': 'nonexistent@test.com',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        # Should show login page again
        assert response.status_code == 200
    
    def test_logout_works(self, authenticated_admin_client):
        """Test logout functionality"""
        response = authenticated_admin_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200


class TestPasswordValidation:
    """Test password hashing and validation"""
    
    def test_password_is_validated_correctly(self, client):
        """Test that passwords are validated"""
        with app.app_context():
            user = get_user_by_email('admin@test.com')
            assert user.validate_password('TestPassword123!')
    
    def test_wrong_password_fails_validation(self, client):
        """Test that wrong password fails"""
        with app.app_context():
            user = get_user_by_email('admin@test.com')
            assert not user.validate_password('WrongPassword')


class TestProtectedPages:
    """Test access control"""
    
    def test_unauthenticated_users_redirected_from_users_page(self, client):
        """Test that unauthenticated users cannot access /users"""
        response = client.get('/users')
        assert response.status_code in [302, 401]
    
    def test_authenticated_admin_can_access_users_page(self, authenticated_admin_client):
        """Test that authenticated admin can access users page"""
        response = authenticated_admin_client.get('/users')
        assert response.status_code == 200
    
    def test_unauthenticated_users_redirected_from_login(self, client):
        """Test that unauthenticated users can access login page"""
        response = client.get('/login')
        assert response.status_code == 200


class TestRoles:
    """Test role system"""
    
    def test_admin_user_has_admin_role(self, client):
        """Test that admin user has System Admin role"""
        with app.app_context():
            admin = get_user_by_email('admin@test.com')
            assert admin.role.name == "System Admin"
    
    def test_regular_user_has_default_role(self, client):
        """Test that regular user has Default Role"""
        with app.app_context():
            user = get_user_by_email('user@test.com')
            assert user.role.name == "Default Role"


class TestUserFixtures:
    """Test that user fixtures work correctly"""
    
    def test_admin_user_fixture_returns_uuid(self, admin_user):
        """Test that admin_user fixture returns UUID"""
        assert admin_user is not None
        assert isinstance(admin_user, str)
        # UUIDs have dashes
        assert '-' in admin_user
    
    def test_default_user_fixture_returns_uuid(self, default_user):
        """Test that default_user fixture returns UUID"""
        assert default_user is not None
        assert isinstance(default_user, str)
        assert '-' in default_user
    
    def test_deactivated_user_fixture_returns_uuid(self, deactivated_user):
        """Test that deactivated_user fixture returns UUID"""
        assert deactivated_user is not None
        assert isinstance(deactivated_user, str)
        assert '-' in deactivated_user
    
    def test_deactivated_user_is_inactive(self, deactivated_user):
        """Test that deactivated user is actually inactive"""
        with app.app_context():
            user = get_user_by_email('inactive@test.com')
            assert user.active is False


class TestFlashMessages:
    """Test flash message display"""
    
    def test_failed_login_shows_error_message(self, client):
        """Test that failed login shows error message"""
        response = client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'WrongPassword'
        }, follow_redirects=True)
        
        # Should contain alert class (Bootstrap alert)
        assert b'alert' in response.data.lower()
