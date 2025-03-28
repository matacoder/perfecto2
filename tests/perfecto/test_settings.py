import pytest
import os
from django.conf import settings
from pathlib import Path

class TestProjectSettings:
    
    def test_installed_apps_configuration(self):
        """Test that all required apps are installed"""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'accounts',
            'companies',
            'teams',
            'reviews',
            'invitations',
            'rest_framework',
            'django_htmx',
            'crispy_forms',
            'crispy_bulma',
        ]
        
        for app in required_apps:
            assert app in settings.INSTALLED_APPS
    
    def test_middleware_configuration(self):
        """Test that all required middleware is installed"""
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'whitenoise.middleware.WhiteNoiseMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django_htmx.middleware.HtmxMiddleware',
        ]
        
        for middleware in required_middleware:
            assert middleware in settings.MIDDLEWARE
    
    def test_templates_configuration(self):
        """Test that templates are properly configured"""
        template_dirs = settings.TEMPLATES[0]['DIRS']
        project_dir = Path(settings.BASE_DIR)
        templates_dir = os.path.join(project_dir, 'templates')
        
        assert any(str(templates_dir) in str(path) for path in template_dirs)
    
    def test_static_files_configuration(self):
        """Test static files configuration"""
        assert settings.STATIC_URL == '/static/'
        assert 'whitenoise.storage.CompressedManifestStaticFilesStorage' == settings.STATICFILES_STORAGE
    
    def test_auth_configuration(self):
        """Test authentication configuration"""
        assert settings.AUTH_USER_MODEL == 'accounts.User'
        assert settings.LOGIN_URL == 'login'
        assert settings.LOGIN_REDIRECT_URL == 'dashboard'
        assert settings.LOGOUT_REDIRECT_URL == 'home'
    
    def test_localization_settings(self):
        """Test localization settings"""
        assert settings.LANGUAGE_CODE == 'ru-ru'
        assert settings.TIME_ZONE == 'Europe/Moscow'
        assert settings.USE_I18N is True
        assert settings.USE_TZ is True
