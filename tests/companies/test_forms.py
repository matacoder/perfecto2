import pytest
from django.core.exceptions import ValidationError
from accounts.models import User
from companies.forms import CompanyForm, CompanyUserForm

@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com",
        password="password123",
        user_name="Test User"
    )

@pytest.fixture
def another_user():
    return User.objects.create_user(
        email="another@example.com",
        password="password456",
        user_name="Another User"
    )

@pytest.mark.django_db
class TestCompanyForm:
    
    def test_valid_company_form(self):
        """Test that a form with valid data is valid"""
        form_data = {
            'company_name': 'Test Company',
            'company_description': 'This is a test company'
        }
        form = CompanyForm(data=form_data)
        assert form.is_valid() is True
    
    def test_blank_company_name(self):
        """Test that company_name is required"""
        form_data = {
            'company_name': '',
            'company_description': 'This is a test company'
        }
        form = CompanyForm(data=form_data)
        assert form.is_valid() is False
        assert 'company_name' in form.errors
    
    def test_company_form_widgets(self):
        """Test that the form uses the expected widgets"""
        form = CompanyForm()
        assert 'rows' in form.fields['company_description'].widget.attrs
        assert form.fields['company_description'].widget.attrs['rows'] == 4

@pytest.mark.django_db
class TestCompanyUserForm:
    
    def test_valid_company_user_form(self, user):
        """Test that a form with valid data is valid"""
        form_data = {
            'user': user.id,
            'is_manager': True
        }
        form = CompanyUserForm(data=form_data)
        assert form.is_valid() is True
    
    def test_blank_user(self, user):
        """Test that user is required"""
        form_data = {
            'user': '',
            'is_manager': True
        }
        form = CompanyUserForm(data=form_data)
        assert form.is_valid() is False
        assert 'user' in form.errors
    
    def test_queryset_contains_users(self, user, another_user):
        """Test that the user queryset contains the expected users"""
        form = CompanyUserForm()
        assert user in form.fields['user'].queryset
        assert another_user in form.fields['user'].queryset
    
    def test_is_manager_default_value(self):
        """Test that is_manager defaults to False"""
        form = CompanyUserForm()
        assert form.fields['is_manager'].initial is False
        assert form.fields['is_manager'].required is False
