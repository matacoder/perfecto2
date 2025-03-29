from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reviews.views import (
    perfreview_list,  # Исправленное имя функции (было perfreviews_list)
    perfreviews_create,
    perfreview_detail,
    achievement_create,
    achievement_score
)

class TestReviewUrls(SimpleTestCase):
    
    def test_perfreview_list_url(self):
        url = reverse('perfreview_list')
        self.assertEqual(resolve(url).func, perfreview_list)
    
    def test_perfreview_create_team_url(self):
        url = reverse('perfreview_create_team', kwargs={'team_id': 1})
        self.assertEqual(resolve(url).func, perfreviews_create)
    
    def test_perfreview_create_user_url(self):
        url = reverse('perfreview_create_user', kwargs={'team_id': 1, 'user_id': 1})
        self.assertEqual(resolve(url).func, perfreviews_create)
    
    def test_perfreview_detail_url(self):
        url = reverse('perfreview_detail', kwargs={'review_id': 1})
        self.assertEqual(resolve(url).func, perfreview_detail)
    
    def test_achievement_create_url(self):
        url = reverse('achievement_create', kwargs={'review_id': 1})
        self.assertEqual(resolve(url).func, achievement_create)
    
    def test_achievement_score_url(self):
        url = reverse('achievement_score', kwargs={'achievement_id': 1})
        self.assertEqual(resolve(url).func, achievement_score)
