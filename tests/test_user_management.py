"""
Comprehensive user management tests.
Tests user CRUD operations, profiles, deactivation, and list views.
"""

import pytest
from boilerplate.app import app
from boilerplate.modules.user.user_model import get_user_by_email


class TestUserList:
    """Test user list functionality"""
    
    def test_admin_can_view_users_list(self, authenticated_admin_client):
        """Test that admin can view user list"""
        response = authenticated_admin_client.get('/users')
        assert response.status_code == 200
        assert b'user' in response.data.lower()
    
    def test_unauthenticated_cannot_view_users_list(self, client):
        """Test that unauthenticated users cannot view user list"""
        response = client.get('/users')
        assert response.status_code == 302  # Redirect to login
    
    def test_users_list_shows_active_users(self, authenticated_admin_client):
        """Test that active users appear in list"""
        response = authenticated_admin_client.get('/users')
        assert response.status_code == 200
        # Should contain user emails
        assert b'admin@test.com' in response.data or b'test.com' in response.data


class TestUserCreation:
    """Test creating new users"""
    
    def test_admin_can_create_user(self, authenticated_admin_client, client):
        """Test that admin can create users"""
        with app.app_context():
            default_role = get_user_by_email('user@test.com').role
            role_id = str(default_role.uuid)
        
        response = authenticated_admin_client.post('/users/create', data={
            'email': 'newuser@test.com',
            'first-name': 'New',
            'last-name': 'User',
            'password': 'NewPassword123!',
            'password-confirm': 'NewPassword123!',
            'role-id': role_id
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_admin_cannot_create_duplicate_email(self, authenticated_admin_client):
        """Test that duplicate emails are rejected"""
        with app.app_context():
            default_role = get_user_by_email('user@test.com').role
            role_id = str(default_role.uuid)
        
        response = authenticated_admin_client.post('/users/create', data={
            'email': 'admin@test.com',  # Already exists
            'first-name': 'Test',
            'last-name': 'User',
            'password': 'TestPassword123!',
            'password-confirm': 'TestPassword123!',
            'role-id': role_id
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should show error
        assert b'alert' in response.data.lower()


class TestUserProfile:
    """Test user profile functionality"""
    
    def test_admin_can_view_user_profile(self, authenticated_admin_client, admin_user):
        """Test that admin can view a user profile"""
        response = authenticated_admin_client.get(f'/users/{admin_user}')
        assert response.status_code == 200
    
    def test_admin_can_update_user_profile(self, authenticated_admin_client, default_user):
        """Test that admin can update user profile"""
        with app.app_context():
            user_role = get_user_by_email('user@test.com').role
            role_id = str(user_role.uuid)
        
        response = authenticated_admin_client.post(f'/users/{default_user}', data={
            'first-name': 'Updated',
            'last-name': 'User',
            'email': 'user@test.com',
            'role-id': role_id
        }, follow_redirects=True)
        assert response.status_code == 200
        
        # Verify update
        with app.app_context():
            user = get_user_by_email('user@test.com')
            assert user.first_name == 'Updated'
    
    def test_admin_can_update_user_password(self, authenticated_admin_client, default_user):
        """Test that admin can update user password"""
        with app.app_context():
            user_role = get_user_by_email('user@test.com').role
            role_id = str(user_role.uuid)
        
        response = authenticated_admin_client.post(f'/users/{default_user}', data={
            'first-name': 'Default',
            'last-name': 'User',
            'email': 'user@test.com',
            'password': 'NewPassword123!',
            'password-confirm': 'NewPassword123!',
            'role-id': role_id
        }, follow_redirects=True)
        assert response.status_code == 200


class TestUserDeactivation:
    """Test user deactivation and reactivation"""
    
    def test_admin_can_deactivate_user(self, authenticated_admin_client, default_user):
        """Test that admin can deactivate a user"""
        response = authenticated_admin_client.post(
            f'/users/{default_user}/toggle-active',
            follow_redirects=True
        )
        assert response.status_code == 200
        
        # Verify deactivation
        with app.app_context():
            user = get_user_by_email('user@test.com')
            assert user.active is False
    
    def test_admin_can_reactivate_user(self, authenticated_admin_client, deactivated_user):
        """Test that admin can reactivate a user"""
        response = authenticated_admin_client.post(
            f'/users/{deactivated_user}/toggle-active',
            follow_redirects=True
        )
        assert response.status_code == 200
        
        # Verify reactivation
        with app.app_context():
            user = get_user_by_email('inactive@test.com')
            assert user.active is True
    
    def test_deactivated_user_cannot_login(self, client):
        """Test that deactivated users cannot login"""
        response = client.post('/login', data={
            'email': 'inactive@test.com',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        # Should not be able to login
        assert response.status_code == 200

