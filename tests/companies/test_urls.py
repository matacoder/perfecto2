import pytest
from django.urls import reverse, resolve
from companies.views import company_list, company_create, company_detail, company_add_user

class TestCompanyUrls:
    
    def test_company_list_url(self):
        """Test URL for company list"""
        url = reverse('company_list')
        assert url == '/companies/'
        assert resolve(url).func == company_list
    
    def test_company_create_url(self):
        """Test URL for company create"""
        url = reverse('company_create')
        assert url == '/companies/create/'
        assert resolve(url).func == company_create
    
    def test_company_detail_url(self):
        """Test URL for company detail"""
        url = reverse('company_detail', kwargs={'company_id': 1})
        assert url == '/companies/1/'
        assert resolve(url).func == company_detail
    
    def test_company_add_user_url(self):
        """Test URL for company add user"""
        url = reverse('company_add_user', kwargs={'company_id': 1})
        assert url == '/companies/1/add_user/'
        assert resolve(url).func == company_add_user
