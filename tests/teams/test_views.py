import pytest
from django.urls import reverse
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
def company():
    return Company.objects.create(
        company_name="Test Company",
        company_description="Test Description"
    )

@pytest.fixture
def company_with_manager(company, user):
    CompanyUsers.objects.create(
        user=user,
        company=company,
        is_manager=True,
        is_owner=True
    )
    return company

@pytest.fixture
def company_with_users(company, user, another_user):
    CompanyUsers.objects.create(user=user, company=company, is_manager=True)
    CompanyUsers.objects.create(user=another_user, company=company)
    return company

@pytest.fixture
def team(company):
    return Team.objects.create(
        team_name="Test Team",
        team_description="Test Description",
        company=company
    )

@pytest.fixture
def team_with_users(team, user, another_user):
    TeamUsers.objects.create(user=user, team=team, is_manager=True)
    TeamUsers.objects.create(user=another_user, team=team)
    return team

@pytest.mark.django_db
class TestTeamListView:
    
    def test_team_list_view_authenticated(self, client, user, team):
        """Test that authenticated users can access the team list view"""
        # Add user to the team
        TeamUsers.objects.create(user=user, team=team)
        
        client.force_login(user)
        url = reverse('team_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['teams']) == 1
        assert response.context['teams'][0] == team
    
    def test_team_list_view_unauthenticated(self, client):
        """Test that unauthenticated users are redirected to login"""
        url = reverse('team_list')
        response = client.get(url)
        
        assert response.status_code == 302
        assert '/accounts/login/' in response.url
    
    def test_team_list_view_no_teams(self, client, user):
        """Test that team list view shows no teams if user has none"""
        client.force_login(user)
        url = reverse('team_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['teams']) == 0

@pytest.mark.django_db
class TestTeamCreateView:
    
    def test_team_create_view_get(self, client, user, company_with_manager):
        """Test that company managers can access the team create view"""
        client.force_login(user)
        url = reverse('team_create', kwargs={'company_id': company_with_manager.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['company'] == company_with_manager
    
    def test_team_create_view_post(self, client, user, company_with_manager):
        """Test that company managers can create teams"""
        client.force_login(user)
        url = reverse('team_create', kwargs={'company_id': company_with_manager.id})
        data = {
            'team_name': 'New Team',
            'team_description': 'New Team Description'
        }
        response = client.post(url, data)
        
        assert response.status_code == 302
        assert Team.objects.count() == 1
        
        team = Team.objects.first()
        assert team.team_name == 'New Team'
        assert team.team_description == 'New Team Description'
        assert team.company == company_with_manager
        
        # Check that the user is set as owner and manager of the team
        team_user = TeamUsers.objects.get(user=user, team=team)
        assert team_user.is_owner is True
        assert team_user.is_manager is True
    
    def test_team_create_view_unauthorized(self, client, another_user, company):
        """Test that regular users can't create teams in a company"""
        # Add user to company but not as manager
        CompanyUsers.objects.create(user=another_user, company=company, is_manager=False)
        
        client.force_login(another_user)
        url = reverse('team_create', kwargs={'company_id': company.id})
        response = client.get(url)
        
        assert response.status_code == 403  # Forbidden
    
    def test_team_create_view_unauthenticated(self, client, company):
        """Test that unauthenticated users are redirected to login"""
        url = reverse('team_create', kwargs={'company_id': company.id})
        response = client.get(url)
        
        assert response.status_code == 302
        assert '/accounts/login/' in response.url

@pytest.mark.django_db
class TestTeamDetailView:
    
    def test_team_detail_view_member(self, client, user, team):
        """Test that team members can access the team detail view"""
        TeamUsers.objects.create(user=user, team=team)
        
        client.force_login(user)
        url = reverse('team_detail', kwargs={'team_id': team.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['team'] == team
        assert response.context['is_manager'] is False
        assert response.context['is_owner'] is False
        assert len(response.context['team_users']) == 1
    
    def test_team_detail_view_manager(self, client, user, team):
        """Test that team managers see correct roles in detail view"""
        TeamUsers.objects.create(user=user, team=team, is_manager=True)
        
        client.force_login(user)
        url = reverse('team_detail', kwargs={'team_id': team.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['team'] == team
        assert response.context['is_manager'] is True
        assert response.context['is_owner'] is False
    
    def test_team_detail_view_owner(self, client, user, team):
        """Test that team owners see correct roles in detail view"""
        TeamUsers.objects.create(user=user, team=team, is_manager=True, is_owner=True)
        
        client.force_login(user)
        url = reverse('team_detail', kwargs={'team_id': team.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['team'] == team
        assert response.context['is_manager'] is True
        assert response.context['is_owner'] is True
    
    def test_team_detail_view_company_manager(self, client, user, team, company):
        """Test that company managers can access the team detail view"""
        # Add user as company manager but not team member
        CompanyUsers.objects.create(user=user, company=company, is_manager=True)
        
        client.force_login(user)
        url = reverse('team_detail', kwargs={'team_id': team.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['team'] == team
        assert response.context['is_manager'] is True
        assert response.context['is_owner'] is False
    
    def test_team_detail_view_unauthorized(self, client, another_user, team):
        """Test that unauthorized users get a forbidden response"""
        client.force_login(another_user)
        url = reverse('team_detail', kwargs={'team_id': team.id})
        response = client.get(url)
        
        assert response.status_code == 403  # Forbidden

@pytest.mark.django_db
class TestTeamAddUserView:
    
    def test_team_add_user_view_get(self, client, user, team_with_users):
        """Test that team managers can access the team add user view"""
        client.force_login(user)
        url = reverse('team_add_user', kwargs={'team_id': team_with_users.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['team'] == team_with_users
    
    def test_team_add_user_view_post(self, client, user, another_user, team, company_with_users):
        """Test that team managers can add users to the team"""
        # Make user a team manager
        TeamUsers.objects.create(user=user, team=team, is_manager=True)
        
        client.force_login(user)
        url = reverse('team_add_user', kwargs={'team_id': team.id})
        data = {
            'user': another_user.id,
            'is_manager': True
        }
        response = client.post(url, data)
        
        assert response.status_code == 302
        assert TeamUsers.objects.filter(team=team, user=another_user).exists()
        
        team_user = TeamUsers.objects.get(team=team, user=another_user)
        assert team_user.is_manager is True
        assert team_user.is_owner is False
    
    def test_team_add_user_view_update_existing(self, client, user, another_user, team, company_with_users):
        """Test that managers can update existing users in the team"""
        # Make user a team manager
        TeamUsers.objects.create(user=user, team=team, is_manager=True)
        
        # Create user with manager=False first
        TeamUsers.objects.create(
            user=another_user,
            team=team,
            is_manager=False,
            is_owner=False
        )
        
        client.force_login(user)
        url = reverse('team_add_user', kwargs={'team_id': team.id})
        data = {
            'user': another_user.id,
            'is_manager': True
        }
        response = client.post(url, data)
        
        assert response.status_code == 302
        team_user = TeamUsers.objects.get(team=team, user=another_user)
        assert team_user.is_manager is True  # Should be updated to True
    
    def test_team_add_user_view_unauthorized(self, client, another_user, team):
        """Test that unauthorized users get a forbidden response"""
        client.force_login(another_user)
        url = reverse('team_add_user', kwargs={'team_id': team.id})
        response = client.get(url)
        
        assert response.status_code == 403  # Forbidden
