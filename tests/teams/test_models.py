import pytest
from django.db import IntegrityError
from accounts.models import User
from companies.models import Company
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
        company_description="Test Company Description"
    )

@pytest.fixture
def team(company):
    return Team.objects.create(
        team_name="Test Team",
        team_description="Test Team Description",
        company=company
    )

@pytest.fixture
def team_user(user, team):
    return TeamUsers.objects.create(
        user=user,
        team=team,
        is_manager=True,
        is_owner=True
    )

@pytest.mark.django_db
class TestTeamModel:
    
    def test_team_creation(self, team, company):
        """Test that a team can be created with the expected fields"""
        assert team.team_name == "Test Team"
        assert team.team_description == "Test Team Description"
        assert team.company == company
        assert team.created is not None
        assert team.edited is not None
    
    def test_team_string_representation(self, team):
        """Test the string representation of a team"""
        assert str(team) == "Test Team"
    
    def test_team_with_users(self, team, user, another_user):
        """Test that users can be associated with a team"""
        TeamUsers.objects.create(user=user, team=team)
        TeamUsers.objects.create(user=another_user, team=team)
        
        assert team.users.count() == 2
        assert user in team.users.all()
        assert another_user in team.users.all()

@pytest.mark.django_db
class TestTeamUsersModel:
    
    def test_team_user_creation(self, team_user, user, team):
        """Test that a team user can be created with the expected fields"""
        assert team_user.user == user
        assert team_user.team == team
        assert team_user.is_manager is True
        assert team_user.is_owner is True
    
    def test_team_user_string_representation(self, team_user, user, team):
        """Test the string representation of a team user"""
        assert str(team_user) == f"{user.email} - {team.team_name}"
    
    def test_team_user_unique_constraint(self, user, team):
        """Test that a user can only be associated with a team once"""
        TeamUsers.objects.create(user=user, team=team)
        
        with pytest.raises(IntegrityError):
            TeamUsers.objects.create(user=user, team=team)
    
    def test_team_user_default_values(self, user, team):
        """Test default values for is_manager and is_owner"""
        team_user = TeamUsers.objects.create(user=user, team=team)
        assert team_user.is_manager is False
        assert team_user.is_owner is False
    
    def test_team_user_verbose_name_plural(self):
        """Test that the verbose name plural is set correctly"""
        assert TeamUsers._meta.verbose_name_plural == "Team Users"
