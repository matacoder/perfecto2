import pytest
from perfecto.wsgi import application
from django.core.handlers.wsgi import WSGIHandler

def test_wsgi_application():
    """Test that WSGI application is a Django WSGIHandler"""
    assert isinstance(application, WSGIHandler)
