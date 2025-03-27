from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('telegram-login/', views.telegram_login_request, name='telegram_login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
