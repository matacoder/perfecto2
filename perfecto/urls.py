from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('companies/', include('companies.urls')),
    path('teams/', include('teams.urls')),
    path('reviews/', include('reviews.urls')),
]
