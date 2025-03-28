import pytest
from django.forms import CheckboxSelectMultiple
from accounts.models import User
from teams.models import Team
from companies.models import Company, CompanyUsers
from reviews.models import PerfReview
from reviews.forms import PerfReviewForm, AchievementForm, AchievementScoreForm

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

@pytest.fixture
def team(company):
    return Team.objects.create(
        team_name="Test Team",
        team_description="Test Description",
        company=company
    )

@pytest.fixture
def perfreview(user, team):
    return PerfReview.objects.create(
        user=user,
        team=team
    )

@pytest.mark.django_db
class TestPerfReviewForm:
    
    def test_perfreview_form_fields(self):
        """Test that the form has no editable fields"""
        form = PerfReviewForm()
        assert len(form.fields) == 0

@pytest.mark.django_db
class TestAchievementForm:
    
    def test_achievement_form_fields(self, team, company_with_users, user, another_user):
        """Test that the form has the expected fields"""
        form = AchievementForm(team=team)
        
        assert 'title' in form.fields
        assert 'self_score' in form.fields
        assert 'reviewers' in form.fields
        
        # Check that reviewers field is a multiple choice field with checkbox widget
        assert isinstance(form.fields['reviewers'].widget, CheckboxSelectMultiple)
        
        # Check that the queryset includes users from the company
        reviewers_queryset = form.fields['reviewers'].queryset
        assert user in reviewers_queryset
        assert another_user in reviewers_queryset
    
    def test_achievement_form_without_team(self):
        """Test form behavior when team is not provided"""
        form = AchievementForm()
        assert form.fields['reviewers'].queryset.count() == 0
    
    def test_achievement_form_is_valid(self, team):
        """Test form validation with valid data"""
        form_data = {
            'title': 'Test Achievement',
            'self_score': 4,
            'reviewers': []  # No reviewers
        }
        form = AchievementForm(data=form_data, team=team)
        assert form.is_valid() is True
    
    def test_achievement_form_required_fields(self, team):
        """Test validation with missing required fields"""
        form_data = {
            'title': '',  # Empty title
            'self_score': 4
        }
        form = AchievementForm(data=form_data, team=team)
        assert form.is_valid() is False
        assert 'title' in form.errors
        
        form_data = {
            'title': 'Test Achievement',
            'self_score': None  # Missing score
        }
        form = AchievementForm(data=form_data, team=team)
        assert form.is_valid() is False
        assert 'self_score' in form.errors

@pytest.mark.django_db
class TestAchievementScoreForm:
    
    def test_achievement_score_form_fields(self):
        """Test that the form has the expected fields"""
        form = AchievementScoreForm()
        
        assert 'score' in form.fields
        assert 'comment' in form.fields
        
        # Check that comment field has the expected widget attributes
        assert 'rows' in form.fields['comment'].widget.attrs
        assert form.fields['comment'].widget.attrs['rows'] == 3
    
    def test_achievement_score_form_is_valid(self):
        """Test form validation with valid data"""
        form_data = {
            'score': 4,
            'comment': 'Good job!'
        }
        form = AchievementScoreForm(data=form_data)
        assert form.is_valid() is True
    
    def test_achievement_score_form_required_fields(self):
        """Test validation with missing required fields"""
        form_data = {
            'score': None,  # Missing score
            'comment': 'Good job!'
        }
        form = AchievementScoreForm(data=form_data)
        assert form.is_valid() is False
        assert 'score' in form.errors
    
    def test_achievement_score_form_optional_fields(self):
        """Test validation with missing optional fields"""
        form_data = {
            'score': 4,
            'comment': ''  # Empty comment is valid
        }
        form = AchievementScoreForm(data=form_data)
        assert form.is_valid() is True
