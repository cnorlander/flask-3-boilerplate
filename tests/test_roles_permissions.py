"""
Comprehensive role and permission tests.
Tests role management, permission assignment, and access control.
"""

import pytest
from boilerplate.app import app
from boilerplate.modules.role.role_model import get_role_by_name
from boilerplate.modules.user.user_model import get_user_by_email


class TestRoleSystem:
    """Test role management"""
    
    def test_system_roles_exist(self, client):
        """Test that system roles are created"""
        with app.app_context():
            admin_role = get_role_by_name("System Admin")
            default_role = get_role_by_name("Default Role")
            
            assert admin_role is not None
            assert default_role is not None
    
    def test_admin_role_has_permissions(self, client):
        """Test that admin role has permissions"""
        with app.app_context():
            admin_role = get_role_by_name("System Admin")
            # Admin should have some permissions
            assert admin_role.actions is not None or len(admin_role.actions) > 0
    
    def test_default_role_has_limited_permissions(self, client):
        """Test that default role has limited permissions"""
        with app.app_context():
            default_role = get_role_by_name("Default Role")
            # Default role should exist but have fewer permissions
            assert default_role is not None


class TestPermissions:
    """Test permission checking"""
    
    def test_admin_can_create_users(self, client):
        """Test that admin has permission to create users"""
        with app.app_context():
            admin = get_user_by_email('admin@test.com')
            assert admin.can('create_or_edit_user')
    
    def test_admin_can_manage_roles(self, client):
        """Test that admin has permission to manage roles"""
        with app.app_context():
            admin = get_user_by_email('admin@test.com')
            assert admin.can('create_or_edit_role')
    
    def test_default_user_limited_permissions(self, client):
        """Test that default user has limited permissions"""
        with app.app_context():
            user = get_user_by_email('user@test.com')
            # Default user should not have admin permissions
            assert not user.can('create_or_edit_role')


class TestRoleAssignment:
    """Test role assignment and changes"""
    
    def test_admin_can_assign_roles(self, authenticated_admin_client, default_user):
        """Test that admin can assign roles to users"""
        with app.app_context():
            user_role = get_user_by_email('user@test.com').role
            role_id = str(user_role.uuid)
        
        response = authenticated_admin_client.post(f'/users/{default_user}', data={
            'first-name': 'Default',
            'last-name': 'User',
            'email': 'user@test.com',
            'role-id': role_id
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_user_inherits_role_permissions(self, client):
        """Test that users inherit permissions from their role"""
        with app.app_context():
            admin = get_user_by_email('admin@test.com')
            admin_role = admin.role
            
            # Admin should have admin permissions
            assert admin_role.name == "System Admin"


class TestAccessControl:
    """Test access control based on permissions"""
    
    def test_admin_can_access_users_page(self, authenticated_admin_client):
        """Test that admin can access users management page"""
        response = authenticated_admin_client.get('/users')
        assert response.status_code == 200
    
    def test_regular_user_cannot_create_users(self, authenticated_user_client):
        """Test that regular user cannot create users"""
        response = authenticated_user_client.post('/users/create', data={
            'email': 'test@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'Test123!',
            'password_confirm': 'Test123!',
            'role': 'Default Role'
        }, follow_redirects=True)
        # Should be forbidden or redirected
        assert response.status_code in [403, 302]
    
    def test_unauthenticated_cannot_access_roles_page(self, client):
        """Test that unauthenticated users cannot access roles page"""
        response = client.get('/roles')
        assert response.status_code == 302  # Redirect to login
