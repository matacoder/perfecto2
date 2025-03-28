import pytest
from django.urls import reverse, resolve
from teams.views import team_list, team_create, team_detail, team_add_user

class TestTeamUrls:
    
    def test_team_list_url(self):
        """Test URL for team list"""
        url = reverse('team_list')
        assert url == '/teams/'
        assert resolve(url).func == team_list
    
    def test_team_create_url(self):
        """Test URL for team create"""
        url = reverse('team_create', kwargs={'company_id': 1})
        assert url == '/teams/company/1/create/'
        assert resolve(url).func == team_create
    
    def test_team_detail_url(self):
        """Test URL for team detail"""
        url = reverse('team_detail', kwargs={'team_id': 1})
        assert url == '/teams/1/'
        assert resolve(url).func == team_detail
    
    def test_team_add_user_url(self):
        """Test URL for team add user"""
        url = reverse('team_add_user', kwargs={'team_id': 1})
        assert url == '/teams/1/add_user/'
        assert resolve(url).func == team_add_user
