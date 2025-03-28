import pytest
from django.db import IntegrityError
from accounts.models import User
from companies.models import Company, CompanyUsers

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
        company_description="Test Company Description"
    )

@pytest.fixture
def company_user(user, company):
    return CompanyUsers.objects.create(
        user=user,
        company=company,
        is_manager=True,
        is_owner=True
    )

@pytest.mark.django_db
class TestCompanyModel:
    
    def test_company_creation(self, company):
        """Test that a company can be created with the expected fields"""
        assert company.company_name == "Test Company"
        assert company.company_description == "Test Company Description"
        assert company.created is not None
        assert company.edited is not None
    
    def test_company_string_representation(self, company):
        """Test the string representation of a company"""
        assert str(company) == "Test Company"
    
    def test_company_verbose_name_plural(self):
        """Test that the verbose name plural is set correctly"""
        assert Company._meta.verbose_name_plural == "Companies"
    
    def test_company_with_users(self, company, user, another_user):
        """Test that users can be associated with a company"""
        CompanyUsers.objects.create(user=user, company=company)
        CompanyUsers.objects.create(user=another_user, company=company)
        
        assert company.users.count() == 2
        assert user in company.users.all()
        assert another_user in company.users.all()

@pytest.mark.django_db
class TestCompanyUsersModel:
    
    def test_company_user_creation(self, company_user, user, company):
        """Test that a company user can be created with the expected fields"""
        assert company_user.user == user
        assert company_user.company == company
        assert company_user.is_manager is True
        assert company_user.is_owner is True
    
    def test_company_user_string_representation(self, company_user, user, company):
        """Test the string representation of a company user"""
        assert str(company_user) == f"{user.email} - {company.company_name}"
    
    def test_company_user_unique_constraint(self, user, company):
        """Test that a user can only be associated with a company once"""
        CompanyUsers.objects.create(user=user, company=company)
        
        with pytest.raises(IntegrityError):
            CompanyUsers.objects.create(user=user, company=company)
    
    def test_company_user_default_values(self, user, company):
        """Test default values for is_manager and is_owner"""
        company_user = CompanyUsers.objects.create(user=user, company=company)
        assert company_user.is_manager is False
        assert company_user.is_owner is False
    
    def test_company_user_verbose_name_plural(self):
        """Test that the verbose name plural is set correctly"""
        assert CompanyUsers._meta.verbose_name_plural == "Company Users"
