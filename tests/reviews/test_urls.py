import pytest
from django.urls import reverse, resolve
from reviews.views import (
    perfreviews_list,
    perfreviews_create,
    perfreview_detail,
    achievement_create,
    achievement_score
)

class TestReviewUrls:
    
    def test_perfreview_list_url(self):
        """Test URL for review list"""
        url = reverse('perfreview_list')
        assert url == '/reviews/'
        assert resolve(url).func == perfreviews_list
    
    def test_perfreview_create_team_url(self):
        """Test URL for creating team reviews"""
        url = reverse('perfreview_create_team', kwargs={'team_id': 1})
        assert url == '/reviews/team/1/create/'
        assert resolve(url).func == perfreviews_create
    
    def test_perfreview_create_user_url(self):
        """Test URL for creating user review"""
        url = reverse('perfreview_create_user', kwargs={'team_id': 1, 'user_id': 2})
        assert url == '/reviews/team/1/user/2/create/'
        assert resolve(url).func == perfreviews_create
    
    def test_perfreview_detail_url(self):
        """Test URL for review detail"""
        url = reverse('perfreview_detail', kwargs={'review_id': 1})
        assert url == '/reviews/1/'
        assert resolve(url).func == perfreview_detail
    
    def test_achievement_create_url(self):
        """Test URL for achievement creation"""
        url = reverse('achievement_create', kwargs={'review_id': 1})
        assert url == '/reviews/1/achievement/create/'
        assert resolve(url).func == achievement_create
    
    def test_achievement_score_url(self):
        """Test URL for scoring achievement"""
        url = reverse('achievement_score', kwargs={'achievement_id': 1})
        assert url == '/reviews/achievement/1/score/'
        assert resolve(url).func == achievement_score
