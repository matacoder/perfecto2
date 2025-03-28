from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

# Health check endpoint для проверки работоспособности приложения
def health_check(request):
    """
    Проверка работоспособности приложения.
    Используется для health check в Docker и мониторинга.
    """
    return JsonResponse({
        "status": "ok",
        "app": "perfecto",
        "version": "1.0.0"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('companies/', include('companies.urls')),
    path('teams/', include('teams.urls')),
    path('reviews/', include('reviews.urls')),
    path('invitations/', include('invitations.urls')),
    path('health-check/', health_check, name='health_check'),
]

# Добавляем обслуживание статических и медиа файлов только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
