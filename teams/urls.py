from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('company/<int:company_id>/create/', views.team_create, name='team_create'),
    path('<int:team_id>/', views.team_detail, name='team_detail'),
    path('<int:team_id>/add_user/', views.team_add_user, name='team_add_user'),
]
