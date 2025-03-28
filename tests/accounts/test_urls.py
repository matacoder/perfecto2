import pytest
from django.urls import reverse, resolve
from accounts.views import (
    home_view,
    register_view,
    login_view,
    telegram_login_request,
    dashboard_view
)
from django.contrib.auth.views import LogoutView

class TestAccountsUrls:
    
    def test_home_url(self):
        """Test URL for home page"""
        url = reverse('home')
        assert url == '/'
        assert resolve(url).func == home_view
    
    def test_register_url(self):
        """Test URL for registration"""
        url = reverse('register')
        assert url == '/accounts/register/'
        assert resolve(url).func == register_view
    
    def test_login_url(self):
        """Test URL for login"""
        url = reverse('login')
        assert url == '/accounts/login/'
        assert resolve(url).func == login_view
    
    def test_logout_url(self):
        """Test URL for logout"""
        url = reverse('logout')
        assert url == '/accounts/logout/'
        assert resolve(url).func.__name__ == LogoutView.as_view().__name__
    
    def test_telegram_login_request_url(self):
        """Test URL for telegram login request"""
        # Fix the expected URL path to match the actual implementation
        url = reverse('telegram_login')
        assert url == '/accounts/telegram-login/'
        assert resolve(url).func == telegram_login_request
    
    def test_dashboard_url(self):
        """Test URL for dashboard"""
        url = reverse('dashboard')
        assert url == '/accounts/dashboard/'
        assert resolve(url).func == dashboard_view
