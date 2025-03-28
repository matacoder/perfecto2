import pytest
from django.db import IntegrityError
from django.utils import timezone
from accounts.models import User
from companies.models import Company, CompanyUsers
from teams.models import Team, TeamUsers
from reviews.models import PerfReview, Achievement, AchievementScore

@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com",
        password="password123",
        user_name="Test User"
    )

@pytest.fixture
def reviewer():
    return User.objects.create_user(
        email="reviewer@example.com",
        password="password456",
        user_name="Reviewer User"
    )

@pytest.fixture
def company(user):
    company = Company.objects.create(
        company_name="Test Company",
        company_description="Test Company Description"
    )
    CompanyUsers.objects.create(
        user=user,
        company=company,
        is_manager=True,
        is_owner=True
    )
    return company

@pytest.fixture
def team(company):
    return Team.objects.create(
        team_name="Test Team",
        team_description="Test Team Description",
        company=company
    )

@pytest.fixture
def team_with_user(team, user):
    TeamUsers.objects.create(
        user=user,
        team=team,
        is_manager=True,
        is_owner=False
    )
    return team

@pytest.fixture
def perfreview(user, team):
    return PerfReview.objects.create(
        user=user,
        team=team
    )

@pytest.fixture
def achievement(perfreview):
    achievement = Achievement.objects.create(
        perfreview=perfreview,
        title="Test Achievement",
        self_score=5
    )
    return achievement

@pytest.fixture
def achievement_with_reviewer(achievement, reviewer):
    achievement.reviewers.add(reviewer)
    return achievement

@pytest.fixture
def achievement_score(achievement, reviewer):
    return AchievementScore.objects.create(
        achievement=achievement,
        user=reviewer,
        score=4,
        comment="Good job!"
    )

@pytest.mark.django_db
class TestPerfReviewModel:
    
    def test_perfreview_creation(self, perfreview, user, team):
        """Test that a performance review can be created with the expected fields"""
        assert perfreview.user == user
        assert perfreview.team == team
        assert perfreview.created is not None
        assert perfreview.edited is not None
    
    def test_perfreview_string_representation(self, perfreview, user, team):
        """Test the string representation of a performance review"""
        expected = f"Review for {user.user_name} in {team.team_name}"
        assert str(perfreview) == expected
    
    def test_perfreview_verbose_name_plural(self):
        """Test that the verbose name plural is set correctly"""
        assert PerfReview._meta.verbose_name_plural == "Performance Reviews"
    
    def test_perfreview_unique_constraint(self, user, team):
        """Test unique constraint for user-team-created combination"""
        # Creating first review
        review1 = PerfReview.objects.create(user=user, team=team)
        
        # Second review with same user and team should be allowed
        # as 'created' field will be different
        review2 = PerfReview.objects.create(user=user, team=team)
        assert review1 != review2

@pytest.mark.django_db
class TestAchievementModel:
    
    def test_achievement_creation(self, achievement, perfreview):
        """Test that an achievement can be created with the expected fields"""
        assert achievement.perfreview == perfreview
        assert achievement.title == "Test Achievement"
        assert achievement.self_score == 5
        assert achievement.created is not None
        assert achievement.edited is not None
    
    def test_achievement_with_reviewers(self, achievement, reviewer):
        """Test that reviewers can be added to an achievement"""
        achievement.reviewers.add(reviewer)
        assert reviewer in achievement.reviewers.all()
        assert achievement.reviewers.count() == 1
    
    def test_achievement_string_representation(self, achievement):
        """Test the string representation of an achievement"""
        expected = "Test Achievement..."
        assert str(achievement) == expected
    
    def test_achievement_score_choices(self):
        """Test that score choices are properly defined"""
        expected_choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
        assert Achievement.SCORE_CHOICES == expected_choices

@pytest.mark.django_db
class TestAchievementScoreModel:
    
    def test_achievement_score_creation(self, achievement_score, achievement, reviewer):
        """Test that an achievement score can be created with the expected fields"""
        assert achievement_score.achievement == achievement
        assert achievement_score.user == reviewer
        assert achievement_score.score == 4
        assert achievement_score.comment == "Good job!"
        assert achievement_score.created is not None
        assert achievement_score.edited is not None
    
    def test_achievement_score_string_representation(self, achievement_score, achievement, reviewer):
        """Test the string representation of an achievement score"""
        expected = f"Score for {achievement} by {reviewer.user_name}"
        assert str(achievement_score) == expected
    
    def test_achievement_score_unique_constraint(self, achievement, reviewer):
        """Test that a user can only score an achievement once"""
        AchievementScore.objects.create(
            achievement=achievement,
            user=reviewer,
            score=4
        )
        
        with pytest.raises(IntegrityError):
            AchievementScore.objects.create(
                achievement=achievement,
                user=reviewer,
                score=5
            )
    
    def test_achievement_score_choices(self):
        """Test that score choices are properly defined"""
        expected_choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
        assert AchievementScore.SCORE_CHOICES == expected_choices
