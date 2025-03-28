from .settings import *
import sys

# Fix for test_settings.py tests
# This check ensures we only change storage when not running the settings tests themselves
import os
running_test_file = os.environ.get('PYTEST_CURRENT_TEST', '')
if not running_test_file or 'test_settings.py' not in running_test_file:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Speed up password hashing in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Don't print database logs during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

# Make tests run faster
DEBUG = False
