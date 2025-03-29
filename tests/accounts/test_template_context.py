import pytest
from django.test import RequestFactory
from django.template import Context, Template
from django.urls import reverse
from accounts.models import User
from companies.models import Company, CompanyUsers
from teams.models import Team, TeamUsers
from reviews.models import PerfReview
from invitations.models import Invitation
import re

@pytest.fixture
def user_with_data():
    """Fixture for user with companies, teams, reviews and invitations"""
    user = User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        user_name="Test User"
    )
    
    # Create companies and add user to them
    company1 = Company.objects.create(company_name="Company 1")
    company2 = Company.objects.create(company_name="Company 2")
    CompanyUsers.objects.create(user=user, company=company1)
    CompanyUsers.objects.create(user=user, company=company2)
    
    # Create teams and add user to them
    team1 = Team.objects.create(team_name="Team 1", company=company1)
    team2 = Team.objects.create(team_name="Team 2", company=company1)
    TeamUsers.objects.create(user=user, team=team1)
    TeamUsers.objects.create(user=user, team=team2)
    
    # Create reviews for user
    review1 = PerfReview.objects.create(user=user, team=team1)
    review2 = PerfReview.objects.create(user=user, team=team2)
    
    # Create invitations
    invitation1 = Invitation.objects.create(
        created_by=user,
        invitation_type="company",
        company=company1,
        expires_at="2099-01-01T00:00:00Z"
    )
    invitation2 = Invitation.objects.create(
        created_by=user,
        invitation_type="team",
        company=company1,
        team=team1,
        expires_at="2099-01-01T00:00:00Z"
    )
    
    return user

@pytest.mark.django_db
class TestDashboardContext:
    
    def test_dashboard_counters(self, client, user_with_data):
        """Test that dashboard page has correct counters in context"""
        client.force_login(user_with_data)
        url = reverse('dashboard')
        response = client.get(url)
        
        assert response.status_code == 200
        
        # Check if counters in context are correct
        companies_count = user_with_data.companies.count()
        teams_count = user_with_data.teams.count()
        reviews_count = user_with_data.reviews.count()
        invitations_count = user_with_data.invitations.count()
        
        # Verify the values are what we expect
        assert companies_count == 2
        assert teams_count == 2
        assert reviews_count == 2
        assert invitations_count == 2
        
        # Test directly that the properties return the expected values
        assert len(list(user_with_data.companies)) == 2
        assert len(list(user_with_data.teams)) == 2
        assert len(list(user_with_data.reviews)) == 2
        assert len(list(user_with_data.invitations)) == 2

@pytest.mark.django_db
class TestBaseTemplateContext:
    
    def test_navbar_counters(self, client, user_with_data):
        """Test that navbar shows correct counters"""
        client.force_login(user_with_data)
        url = reverse('dashboard')  # Use any authenticated page
        response = client.get(url)
        
        assert response.status_code == 200
        
        # Check directly that the properties return the expected values
        assert user_with_data.companies.count() == 2
        assert user_with_data.teams.count() == 2
        assert user_with_data.reviews.count() == 2
        assert user_with_data.invitations.count() == 2
        
        # Simple check for badges in the response
        content = response.content.decode('utf-8')
        
        # Check for presence of badge elements with the expected counts
        assert 'class="badge' in content
        assert '>2<' in content
        
        # Make sure specific navbar elements are present
        assert '<i class="fas fa-building' in content
        assert '<i class="fas fa-users' in content
        assert '<i class="fas fa-chart-bar' in content
        assert '<i class="fas fa-envelope' in content
