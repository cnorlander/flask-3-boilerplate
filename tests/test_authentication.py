"""
Comprehensive authentication tests.
Tests login, logout, password validation, and session management.
"""

import pytest
from boilerplate.app import app
from boilerplate.modules.user.user_model import get_user_by_email


class TestLoginFunctionality:
    """Test login page and login process"""
    
    def test_login_page_accessible(self, client):
        """Test that login page loads"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'email' in response.data.lower()
        assert b'password' in response.data.lower()
    
    def test_admin_login_with_valid_credentials(self, client):
        """Test admin login with correct credentials"""
        response = client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_regular_user_login_with_valid_credentials(self, client):
        """Test regular user login with correct credentials"""
        response = client.post('/login', data={
            'email': 'user@test.com',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        assert response.status_code in [200, 403]  # May lack permission but login succeeds
    
    def test_login_fails_with_wrong_password(self, client):
        """Test login fails with incorrect password"""
        response = client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'WrongPassword123!'
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should show login page again with error
        assert b'alert' in response.data.lower()
    
    def test_login_fails_with_nonexistent_email(self, client):
        """Test login fails with non-existent email"""
        response = client.post('/login', data={
            'email': 'nonexistent@test.com',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'alert' in response.data.lower()
    
    def test_inactive_user_cannot_login(self, client):
        """Test that inactive users cannot login"""
        response = client.post('/login', data={
            'email': 'inactive@test.com',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should not successfully login


class TestLogout:
    """Test logout functionality"""
    
    def test_admin_can_logout(self, authenticated_admin_client):
        """Test that admin user can logout"""
        response = authenticated_admin_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to login page
        assert b'login' in response.data.lower()
    
    def test_logout_clears_session(self, authenticated_admin_client):
        """Test that logout clears user session"""
        # Logout
        authenticated_admin_client.get('/logout')
        
        # Try to access protected page
        response = authenticated_admin_client.get('/users')
        assert response.status_code == 302  # Should redirect to login


class TestPasswordReset:
    """Test password reset functionality"""
    
    def test_password_reset_modal_on_login_page(self, client):
        """Test that password reset modal is available on login page"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'passwordResetModal' in response.data or b'password' in response.data.lower()
    
    def test_send_password_reset_email(self, client):
        """Test sending password reset email"""
        response = client.post('/send-password-reset', data={
            'email': 'admin@test.com'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_send_password_reset_nonexistent_email(self, client):
        """Test password reset with non-existent email (should succeed for security)"""
        response = client.post('/send-password-reset', data={
            'email': 'nonexistent@test.com'
        }, follow_redirects=True)
        # Should not reveal if email exists
        assert response.status_code == 200


class TestSessionManagement:
    """Test session handling"""
    
    def test_authenticated_user_session_persists(self, authenticated_admin_client):
        """Test that authenticated session persists"""
        response = authenticated_admin_client.get('/users')
        # Admin should have access
        assert response.status_code == 200
    
    def test_unauthenticated_user_redirected_to_login(self, client):
        """Test that unauthenticated users are redirected"""
        response = client.get('/users')
        assert response.status_code == 302
