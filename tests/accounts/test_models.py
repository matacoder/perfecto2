import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from accounts.models import User

@pytest.mark.django_db
class TestUserModel:
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            user_name="Test User"
        )
        
        assert user.email == "test@example.com"
        assert user.user_name == "Test User"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password("password123") is True
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="admin123",
            user_name="Admin User"
        )
        
        assert admin_user.email == "admin@example.com"
        assert admin_user.is_active is True
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True
    
    def test_email_required(self):
        """Test that email is required"""
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="test123", user_name="Test User")
    
    def test_email_unique(self):
        """Test that users with duplicate emails are not allowed"""
        User.objects.create_user(
            email="test@example.com",
            password="password123",
            user_name="Test User"
        )
        
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="test@example.com",
                password="password456",
                user_name="Another Test User"
            )
    
    def test_email_normalized(self):
        """Test that email addresses are normalized"""
        email = "test@EXAMPLE.com"
        user = User.objects.create_user(
            email=email,
            password="password123",
            user_name="Test User"
        )
        assert user.email == email.lower()
    
    def test_user_string_representation(self):
        """Test the string representation of a user"""
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            user_name="Test User"
        )
        assert str(user) == "test@example.com"
    
    def test_additional_fields(self):
        """Test additional user fields"""
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            user_name="Test User",
            user_job="Software Developer",
            telegram_username="@testuser",
            telegram_id="12345"
        )
        
        assert user.user_job == "Software Developer"
        assert user.telegram_username == "@testuser"
        assert user.telegram_id == "12345"
