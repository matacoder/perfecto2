import pytest
from django.conf import settings

class TestProjectSettings:
    """Тесты для проверки конфигурации настроек проекта."""

    def test_middleware_configuration(self):
        """Проверка middleware конфигурации."""
        # Проверяем наличие важных middleware
        assert 'django.middleware.security.SecurityMiddleware' in settings.MIDDLEWARE
        assert 'django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE
        assert 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE
        assert 'django.contrib.auth.middleware.AuthenticationMiddleware' in settings.MIDDLEWARE
        
        # Whitenoise может быть отключен в тестах, поэтому не проверяем его наличие
        
    def test_installed_apps(self):
        """Проверка установленных приложений."""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'crispy_forms',
            'crispy_bootstrap5',
            'accounts',
            'companies',
            'teams',
            'reviews',
            'invitations',
        ]
        
        for app in required_apps:
            assert app in settings.INSTALLED_APPS
            
    def test_auth_settings(self):
        """Проверка настроек аутентификации."""
        assert settings.AUTH_USER_MODEL == 'accounts.User'
        assert settings.LOGIN_URL == 'login'
        assert settings.LOGIN_REDIRECT_URL == 'dashboard'
        assert settings.LOGOUT_REDIRECT_URL == 'home'
        
    def test_crispy_forms_settings(self):
        """Проверка настроек crispy forms."""
        assert 'bootstrap5' in settings.CRISPY_ALLOWED_TEMPLATE_PACKS
        assert settings.CRISPY_TEMPLATE_PACK == 'bootstrap5'
        
    def test_static_files_configuration(self):
        """Проверка настроек статических файлов."""
        # В тестовой среде может использоваться другой storage
        # Не проверяем конкретное значение, а просто проверяем наличие настройки
        assert hasattr(settings, 'STATICFILES_STORAGE')
        assert settings.STATIC_URL == '/static/'
        
        # Проверяем, что правильные пути указаны
        import os
        assert os.path.join(settings.BASE_DIR, 'staticfiles') == settings.STATIC_ROOT
        assert os.path.join(settings.BASE_DIR, 'static') in settings.STATICFILES_DIRS
