import pytest
from django.utils import timezone
from datetime import timedelta
from invitations.models import Invitation
from accounts.models import User
from companies.models import Company
from teams.models import Team

@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com",
        password="password123",
        user_name="Test User"
    )

@pytest.fixture
def company(user):
    return Company.objects.create(
        company_name="Test Company",
        company_description="Test Description"
    )

@pytest.fixture
def team(company):
    return Team.objects.create(
        team_name="Test Team",
        team_description="Test Team Description",
        company=company
    )

@pytest.fixture
def company_invitation(user, company):
    return Invitation.objects.create(
        created_by=user,
        invitation_type=Invitation.TYPE_COMPANY,
        company=company,
        expires_at=timezone.now() + timedelta(days=7),
        is_manager_invite=False
    )

@pytest.fixture
def team_invitation(user, company, team):
    return Invitation.objects.create(
        created_by=user,
        invitation_type=Invitation.TYPE_TEAM,
        company=company,
        team=team,
        expires_at=timezone.now() + timedelta(days=7),
        is_manager_invite=True
    )

@pytest.fixture
def expired_invitation(user, company):
    return Invitation.objects.create(
        created_by=user,
        invitation_type=Invitation.TYPE_COMPANY,
        company=company,
        expires_at=timezone.now() - timedelta(days=1),
        is_manager_invite=False
    )

@pytest.mark.django_db
class TestInvitationModel:
    
    def test_company_invitation_creation(self, company_invitation, user, company):
        """Test that a company invitation can be created"""
        assert company_invitation.created_by == user
        assert company_invitation.invitation_type == Invitation.TYPE_COMPANY
        assert company_invitation.company == company
        assert company_invitation.team is None
        assert company_invitation.is_manager_invite is False
        assert company_invitation.is_expired is False
    
    def test_team_invitation_creation(self, team_invitation, user, company, team):
        """Test that a team invitation can be created"""
        assert team_invitation.created_by == user
        assert team_invitation.invitation_type == Invitation.TYPE_TEAM
        assert team_invitation.company == company
        assert team_invitation.team == team
        assert team_invitation.is_manager_invite is True
        assert team_invitation.is_expired is False
    
    def test_expired_invitation(self, expired_invitation):
        """Test that an invitation with past expiration date is marked as expired"""
        assert expired_invitation.is_expired is True
    
    def test_default_expiration(self, user, company):
        """Test that an invitation without explicit expiration gets default value"""
        invitation = Invitation.objects.create(
            created_by=user,
            invitation_type=Invitation.TYPE_COMPANY,
            company=company
        )
        expected_expiration = invitation.created_at + timedelta(days=7)
        # Allow for small timestamp differences (seconds)
        assert abs((invitation.expires_at - expected_expiration).total_seconds()) < 10
        assert invitation.is_expired is False
    
    def test_target_name_property_company(self, company_invitation, company):
        """Test that target_name returns company name for company invitations"""
        assert company_invitation.target_name == company.company_name
    
    def test_target_name_property_team(self, team_invitation, team):
        """Test that target_name returns team name for team invitations"""
        assert team_invitation.target_name == team.team_name
    
    def test_invitation_string_representation_company(self, company_invitation, company):
        """Test that str() method returns correct string for company invitations"""
        expected_str = f"Invitation to {company.company_name} company"
        assert str(company_invitation) == expected_str
    
    def test_invitation_string_representation_team(self, team_invitation, team):
        """Test that str() method returns correct string for team invitations"""
        expected_str = f"Invitation to {team.team_name} team"
        assert str(team_invitation) == expected_str
    
    def test_get_absolute_url(self, company_invitation):
        """Test that get_absolute_url returns correct URL for the invitation"""
        expected_url = f"/invitations/accept/{company_invitation.id}/"
        assert company_invitation.get_absolute_url() == expected_url
