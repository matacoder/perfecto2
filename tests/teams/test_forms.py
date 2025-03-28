import pytest
from django.core.exceptions import ValidationError
from accounts.models import User
from companies.models import Company, CompanyUsers
from teams.models import Team
from teams.forms import TeamForm, TeamUserForm

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

@pytest.fixture
def company():
    return Company.objects.create(
        company_name="Test Company",
        company_description="Test Description"
    )

@pytest.fixture
def company_with_users(company, user, another_user):
    CompanyUsers.objects.create(user=user, company=company)
    CompanyUsers.objects.create(user=another_user, company=company)
    return company

@pytest.mark.django_db
class TestTeamForm:
    
    def test_valid_team_form(self):
        """Test that a form with valid data is valid"""
        form_data = {
            'team_name': 'Test Team',
            'team_description': 'This is a test team'
        }
        form = TeamForm(data=form_data)
        assert form.is_valid() is True
    
    def test_blank_team_name(self):
        """Test that team_name is required"""
        form_data = {
            'team_name': '',
            'team_description': 'This is a test team'
        }
        form = TeamForm(data=form_data)
        assert form.is_valid() is False
        assert 'team_name' in form.errors
    
    def test_team_form_widgets(self):
        """Test that the form uses the expected widgets"""
        form = TeamForm()
        assert 'rows' in form.fields['team_description'].widget.attrs
        assert form.fields['team_description'].widget.attrs['rows'] == 4

@pytest.mark.django_db
class TestTeamUserForm:
    
    def test_team_user_form_with_company(self, user, another_user, company_with_users):
        """Test that form with company provided has correct user queryset"""
        form = TeamUserForm(company=company_with_users)
        user_queryset = form.fields['user'].queryset
        
        assert user in user_queryset
        assert another_user in user_queryset
    
    def test_team_user_form_without_company(self):
        """Test that form without company has empty queryset"""
        form = TeamUserForm()
        assert form.fields['user'].queryset.count() == 0
    
    def test_valid_team_user_form(self, user, company_with_users):
        """Test that a form with valid data is valid"""
        form_data = {
            'user': user.id,
            'is_manager': True
        }
        form = TeamUserForm(data=form_data, company=company_with_users)
        assert form.is_valid() is True
    
    def test_blank_user(self, company_with_users):
        """Test that user is required"""
        form_data = {
            'user': '',
            'is_manager': True
        }
        form = TeamUserForm(data=form_data, company=company_with_users)
        assert form.is_valid() is False
        assert 'user' in form.errors
    
    def test_is_manager_default_value(self, company_with_users):
        """Test that is_manager defaults to False"""
        form = TeamUserForm(company=company_with_users)
        assert form.fields['is_manager'].initial is False
        assert form.fields['is_manager'].required is False
