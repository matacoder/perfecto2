import pytest
from django.urls import reverse, resolve
from django.conf import settings

class TestMainProjectUrls:
    
    def test_home_url_included(self):
        """Test that the home URL is properly configured"""
        url = reverse('home')
        assert url == '/'
    
    def test_admin_url_included(self):
        """Test that admin URL is properly configured"""
        url = reverse('admin:index')
        assert url == '/admin/'
    
    def test_app_urls_included(self):
        """Test that all app URLs are properly included"""
        # Test some key URLs from each app to ensure they're included
        urls_to_test = [
            # accounts app
            reverse('login'),
            reverse('register'),
            reverse('dashboard'),
            
            # companies app
            reverse('company_list'),
            reverse('company_create'),
            
            # teams app
            reverse('team_list'),
            
            # reviews app
            reverse('perfreview_list'),
            
            # invitations app
            reverse('invitation_list')
        ]
        
        # If we can reverse these URLs without exception, 
        # it means they're properly included
        assert len(urls_to_test) == 8
