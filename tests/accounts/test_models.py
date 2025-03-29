import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from accounts.models import User
from companies.models import Company, CompanyUsers
from teams.models import Team, TeamUsers
from reviews.models import PerfReview
from invitations.models import Invitation

@pytest.fixture
def test_user():
    """Create a user for testing properties"""
    return User.objects.create_user(
        email="property_test@example.com",
        password="password123",
        user_name="Property Test User"
    )

@pytest.mark.django_db
class TestUserModel:
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            user_name="Test User"
        )
        
        assert user.email == "test@example.com"
        assert user.user_name == "Test User"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password("password123") is True
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="admin123",
            user_name="Admin User"
        )
        
        assert admin_user.email == "admin@example.com"
        assert admin_user.is_active is True
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True
    
    def test_email_required(self):
        """Test that email is required"""
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="test123", user_name="Test User")
    
    def test_email_unique(self):
        """Test that users with duplicate emails are not allowed"""
        User.objects.create_user(
            email="test@example.com",
            password="password123",
            user_name="Test User"
        )
        
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="test@example.com",
                password="password456",
                user_name="Another Test User"
            )
    
    def test_email_normalized(self):
        """Test that email addresses are normalized"""
        email = "test@EXAMPLE.com"
        user = User.objects.create_user(
            email=email,
            password="password123",
            user_name="Test User"
        )
        assert user.email == email.lower()
    
    def test_user_string_representation(self):
        """Test the string representation of a user"""
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            user_name="Test User"
        )
        assert str(user) == "test@example.com"
    
    def test_additional_fields(self):
        """Test additional user fields"""
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            user_name="Test User",
            user_job="Software Developer",
            telegram_username="@testuser",
            telegram_id="12345"
        )
        
        assert user.user_job == "Software Developer"
        assert user.telegram_username == "@testuser"
        assert user.telegram_id == "12345"
    
    def test_property_companies(self):
        """Test that companies property returns correct queryset"""
        user = User.objects.create_user(
            email="companies_test@example.com",
            password="password123",
            user_name="Companies Test User"
        )
        
        # Create companies
        company1 = Company.objects.create(company_name="Company 1")
        company2 = Company.objects.create(company_name="Company 2")
        
        # Create relations
        relation1 = CompanyUsers.objects.create(user=user, company=company1)
        relation2 = CompanyUsers.objects.create(user=user, company=company2)
        
        # Test property
        companies = user.companies
        assert companies.count() == 2
        assert relation1 in companies
        assert relation2 in companies
    
    def test_property_teams(self):
        """Test that teams property returns correct queryset"""
        user = User.objects.create_user(
            email="teams_test@example.com",
            password="password123",
            user_name="Teams Test User"
        )
        
        # Create company and teams
        company = Company.objects.create(company_name="Test Company")
        team1 = Team.objects.create(team_name="Team 1", company=company)
        team2 = Team.objects.create(team_name="Team 2", company=company)
        
        # Create relations
        relation1 = TeamUsers.objects.create(user=user, team=team1)
        relation2 = TeamUsers.objects.create(user=user, team=team2)
        
        # Test property
        teams = user.teams
        assert teams.count() == 2
        assert relation1 in teams
        assert relation2 in teams
    
    def test_property_reviews(self):
        """Test that reviews property returns correct queryset"""
        user = User.objects.create_user(
            email="reviews_test@example.com",
            password="password123",
            user_name="Reviews Test User"
        )
        
        # Create company and team
        company = Company.objects.create(company_name="Test Company")
        team = Team.objects.create(team_name="Test Team", company=company)
        
        # Create reviews
        review1 = PerfReview.objects.create(user=user, team=team)
        review2 = PerfReview.objects.create(user=user, team=team)
        
        # Test property
        reviews = user.reviews
        assert reviews.count() == 2
        assert review1 in reviews
        assert review2 in reviews
    
    def test_property_invitations(self):
        """Test that invitations property returns correct queryset"""
        user = User.objects.create_user(
            email="invitations_test@example.com",
            password="password123",
            user_name="Invitations Test User"
        )
        
        # Create company
        company = Company.objects.create(company_name="Test Company")
        team = Team.objects.create(team_name="Test Team", company=company)
        
        # Create invitations
        invitation1 = Invitation.objects.create(
            created_by=user,
            invitation_type="company",
            company=company,
            expires_at="2099-01-01T00:00:00Z"
        )
        invitation2 = Invitation.objects.create(
            created_by=user,
            invitation_type="team",
            company=company,
            team=team,
            expires_at="2099-01-01T00:00:00Z"
        )
        
        # Test property
        invitations = user.invitations
        assert invitations.count() == 2
        assert invitation1 in invitations
        assert invitation2 in invitations
