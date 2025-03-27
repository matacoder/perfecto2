import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from invitations.models import Invitation
from accounts.models import User
from companies.models import Company, CompanyUsers
from teams.models import Team, TeamUsers

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
def company(user):
    company = Company.objects.create(
        company_name="Test Company",
        company_description="Test Description"
    )
    CompanyUsers.objects.create(
        user=user,
        company=company,
        is_manager=True,
        is_owner=True
    )
    return company

@pytest.fixture
def team(company, user):
    team = Team.objects.create(
        team_name="Test Team",
        team_description="Test Description",
        company=company
    )
    TeamUsers.objects.create(
        user=user,
        team=team,
        is_manager=True,
        is_owner=True
    )
    return team

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
class TestCreateCompanyInvitation:
    
    def test_create_company_invitation_get(self, client, user, company):
        """Test GET request to create company invitation view"""
        client.force_login(user)
        url = reverse('create_company_invitation', kwargs={'company_id': company.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'company' in response.context
        assert response.context['invitation_type'] == 'компанию'
    
    def test_create_company_invitation_post(self, client, user, company):
        """Test POST request to create company invitation view"""
        client.force_login(user)
        url = reverse('create_company_invitation', kwargs={'company_id': company.id})
        response = client.post(url, {'is_manager_invite': True})
        
        assert response.status_code == 302  # Redirect after successful creation
        assert Invitation.objects.count() == 1
        
        invitation = Invitation.objects.first()
        assert invitation.created_by == user
        assert invitation.company == company
        assert invitation.invitation_type == Invitation.TYPE_COMPANY
        assert invitation.is_manager_invite is True
    
    def test_create_company_invitation_unauthorized(self, client, company):
        """Test that unauthorized users can't access view"""
        url = reverse('create_company_invitation', kwargs={'company_id': company.id})
        response = client.get(url)
        
        assert response.status_code == 302  # Redirect to login
    
    def test_create_company_invitation_forbidden(self, client, another_user, company):
        """Test that users without permission can't create invitations"""
        client.force_login(another_user)
        url = reverse('create_company_invitation', kwargs={'company_id': company.id})
        response = client.get(url)
        
        assert response.status_code == 403  # Forbidden

@pytest.mark.django_db
class TestCreateTeamInvitation:
    
    def test_create_team_invitation_get(self, client, user, team):
        """Test GET request to create team invitation view"""
        client.force_login(user)
        url = reverse('create_team_invitation', kwargs={'team_id': team.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'team' in response.context
        assert response.context['invitation_type'] == 'команду'
    
    def test_create_team_invitation_post(self, client, user, team):
        """Test POST request to create team invitation view"""
        client.force_login(user)
        url = reverse('create_team_invitation', kwargs={'team_id': team.id})
        response = client.post(url, {'is_manager_invite': False})
        
        assert response.status_code == 302  # Redirect after successful creation
        assert Invitation.objects.count() == 1
        
        invitation = Invitation.objects.first()
        assert invitation.created_by == user
        assert invitation.team == team
        assert invitation.invitation_type == Invitation.TYPE_TEAM
        assert invitation.is_manager_invite is False

@pytest.mark.django_db
class TestInvitationAccept:
    
    def test_invitation_accept_get_authenticated(self, client, user, company_invitation):
        """Test GET request to invitation accept view when authenticated"""
        client.force_login(user)
        url = reverse('invitation_accept', kwargs={'uuid': company_invitation.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'invitation' in response.context
        assert 'form' in response.context
    
    def test_invitation_accept_get_unauthenticated(self, client, company_invitation):
        """Test GET request to invitation accept when not authenticated"""
        url = reverse('invitation_accept', kwargs={'uuid': company_invitation.id})
        response = client.get(url)
        
        assert response.status_code == 302  # Redirect to register
        assert 'pending_invitation' in client.session
        assert client.session['pending_invitation'] == str(company_invitation.id)
    
    def test_invitation_accept_expired(self, client, user, expired_invitation):
        """Test GET request to expired invitation"""
        client.force_login(user)
        url = reverse('invitation_accept', kwargs={'uuid': expired_invitation.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'invitation_expired.html' in [t.name for t in response.templates]
    
    def test_accept_company_invitation(self, client, another_user, company_invitation):
        """Test accepting company invitation"""
        client.force_login(another_user)
        url = reverse('invitation_accept', kwargs={'uuid': company_invitation.id})
        response = client.post(url, {'action': 'accept'})
        
        assert response.status_code == 302  # Redirect to company detail
        
        # Check that user was added to company
        company_user = CompanyUsers.objects.filter(
            user=another_user, 
            company=company_invitation.company
        ).first()
        
        assert company_user is not None
        assert company_user.is_manager is False
        assert company_user.is_owner is False
    
    def test_accept_team_invitation(self, client, another_user, team_invitation):
        """Test accepting team invitation"""
        client.force_login(another_user)
        url = reverse('invitation_accept', kwargs={'uuid': team_invitation.id})
        response = client.post(url, {'action': 'accept'})
        
        assert response.status_code == 302  # Redirect to team detail
        
        # Check that user was added to company
        company_user = CompanyUsers.objects.filter(
            user=another_user, 
            company=team_invitation.company
        ).first()
        assert company_user is not None
        
        # Check that user was added to team
        team_user = TeamUsers.objects.filter(
            user=another_user, 
            team=team_invitation.team
        ).first()
        assert team_user is not None
        assert team_user.is_manager is True  # This was a manager invitation
        assert team_user.is_owner is False
    
    def test_decline_invitation(self, client, another_user, company_invitation):
        """Test declining invitation"""
        client.force_login(another_user)
        url = reverse('invitation_accept', kwargs={'uuid': company_invitation.id})
        response = client.post(url, {'action': 'decline'})
        
        assert response.status_code == 302  # Redirect to dashboard
        
        # Check that user wasn't added to company
        company_user = CompanyUsers.objects.filter(
            user=another_user, 
            company=company_invitation.company
        ).first()
        
        assert company_user is None

@pytest.mark.django_db
class TestInvitationList:
    
    def test_invitation_list_view(self, client, user, company_invitation, team_invitation, expired_invitation):
        """Test invitation list view shows active and expired invitations"""
        client.force_login(user)
        url = reverse('invitation_list')
        response = client.get(url)
        
        assert response.status_code == 200
        
        # Check context data
        assert len(response.context['active_invitations']) == 2  # company and team invitation
        assert len(response.context['expired_invitations']) == 1  # expired invitation
        
        # Check that invitation appears in correct list
        active_invitation_ids = [inv.id for inv in response.context['active_invitations']]
        expired_invitation_ids = [inv.id for inv in response.context['expired_invitations']]
        
        assert company_invitation.id in active_invitation_ids
        assert team_invitation.id in active_invitation_ids
        assert expired_invitation.id in expired_invitation_ids
    
    def test_invitation_list_unauthorized(self, client):
        """Test that unauthorized users can't access invitation list"""
        url = reverse('invitation_list')
        response = client.get(url)
        
        assert response.status_code == 302  # Redirect to login
