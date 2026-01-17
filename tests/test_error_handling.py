"""
Error handling and HTTP status code tests.
Tests error pages and proper HTTP responses.
"""

import pytest
from boilerplate.app import app
from boilerplate.modules.user.user_model import get_user_by_email


class TestHttpStatusCodes:
    """Test HTTP status codes"""
    
    def test_login_page_returns_200(self, client):
        """Test that login page returns 200"""
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_nonexistent_page_returns_404(self, client):
        """Test that non-existent pages return 404"""
        response = client.get('/nonexistent-page-xyz')
        assert response.status_code == 404
    
    def test_redirect_on_unauthenticated_access(self, client):
        """Test that unauthenticated access redirects"""
        response = client.get('/users')
        assert response.status_code == 302


class TestErrorPages:
    """Test error page rendering"""
    
    def test_404_error_page(self, client):
        """Test that 404 error page is displayed"""
        response = client.get('/this-does-not-exist')
        assert response.status_code == 404
        # Should contain error information
        assert b'404' in response.data or b'not found' in response.data.lower()
    
    def test_403_error_page_for_forbidden(self, authenticated_user_client):
        """Test that 403 error is shown for forbidden access"""
        response = authenticated_user_client.get('/roles')
        # User without permission should get 403 or redirect
        assert response.status_code in [403, 302]


class TestFlashMessages:
    """Test flash message display in errors"""
    
    def test_login_error_shows_flash_message(self, client):
        """Test that login errors show flash messages"""
        response = client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'WrongPassword'
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should contain alert
        assert b'alert' in response.data.lower()
    
    def test_duplicate_email_shows_error(self, authenticated_admin_client):
        """Test that duplicate email shows error"""
        with app.app_context():
            default_role = get_user_by_email('user@test.com').role
            role_id = str(default_role.uuid)
        
        response = authenticated_admin_client.post('/users/create', data={
            'email': 'admin@test.com',
            'first-name': 'Test',
            'last-name': 'User',
            'password': 'TestPassword123!',
            'password-confirm': 'TestPassword123!',
            'role-id': role_id
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should show error message
        assert b'alert' in response.data.lower()
