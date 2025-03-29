from django.urls import path
from . import views

urlpatterns = [
    path('', views.perfreview_list, name='perfreview_list'),
    path('team/<int:team_id>/create/', views.perfreviews_create, name='perfreview_create_team'),
    path('team/<int:team_id>/user/<int:user_id>/create/', views.perfreviews_create, name='perfreview_create_user'),
    path('<int:review_id>/', views.perfreview_detail, name='perfreview_detail'),
    path('<int:review_id>/achievement/create/', views.achievement_create, name='achievement_create'),
    path('achievement/<int:achievement_id>/score/', views.achievement_score, name='achievement_score'),
]
