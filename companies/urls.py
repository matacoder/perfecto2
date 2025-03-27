from django.urls import path
from . import views

urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('create/', views.company_create, name='company_create'),
    path('<int:company_id>/', views.company_detail, name='company_detail'),
    path('<int:company_id>/add_user/', views.company_add_user, name='company_add_user'),
]
