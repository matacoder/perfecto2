import pytest
from django.urls import reverse
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
def manager():
    return User.objects.create_user(
        email="manager@example.com",
        password="password456",
        user_name="Manager User"
    )

@pytest.fixture
def reviewer():
    return User.objects.create_user(
        email="reviewer@example.com",
        password="password789",
        user_name="Reviewer User"
    )

@pytest.fixture
def company():
    return Company.objects.create(
        company_name="Test Company",
        company_description="Test Description"
    )

@pytest.fixture
def company_with_users(company, user, manager, reviewer):
    CompanyUsers.objects.create(user=user, company=company)
    CompanyUsers.objects.create(user=manager, company=company, is_manager=True)
    CompanyUsers.objects.create(user=reviewer, company=company)
    return company

@pytest.fixture
def team(company):
    return Team.objects.create(
        team_name="Test Team",
        team_description="Test Description",
        company=company
    )

@pytest.fixture
def team_with_users(team, user, manager, reviewer):
    TeamUsers.objects.create(user=user, team=team)
    TeamUsers.objects.create(user=manager, team=team, is_manager=True)
    TeamUsers.objects.create(user=reviewer, team=team)
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
def achievement_score(achievement_with_reviewer, reviewer):
    return AchievementScore.objects.create(
        achievement=achievement_with_reviewer,
        user=reviewer,
        score=4,
        comment="Good job!"
    )

@pytest.mark.django_db
class TestPerfReviewListView:
    
    def test_perfreview_list_authenticated(self, client, user, perfreview):
        """Test that authenticated users can access their performance reviews"""
        client.force_login(user)
        url = reverse('perfreview_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['my_reviews']) == 1
        assert response.context['my_reviews'][0] == perfreview
    
    def test_perfreview_list_unauthenticated(self, client):
        """Test that unauthenticated users are redirected to login"""
        url = reverse('perfreview_list')
        response = client.get(url)
        
        assert response.status_code == 302
        assert '/accounts/login/' in response.url
    
    def test_perfreview_list_reviewer(self, client, reviewer, achievement_with_reviewer):
        """Test that reviewers can see reviews they are reviewing"""
        client.force_login(reviewer)
        url = reverse('perfreview_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['managed_reviews']) == 1
        assert response.context['managed_reviews'][0] == achievement_with_reviewer.perfreview
    
    def test_perfreview_list_manager(self, client, manager, team_with_users, perfreview):
        """Test that managers can see team reviews"""
        client.force_login(manager)
        url = reverse('perfreview_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['team_reviews']) == 1
        assert response.context['team_reviews'][0] == perfreview

@pytest.mark.django_db
class TestPerfReviewCreateView:
    
    def test_perfreview_create_team_as_manager(self, client, manager, team_with_users):
        """Test that managers can create reviews for the entire team"""
        client.force_login(manager)
        url = reverse('perfreview_create_team', kwargs={'team_id': team_with_users.id})
        response = client.get(url)
        
        # Should redirect after creating reviews
        assert response.status_code == 302
        
        # Check if reviews were created for all team members
        assert PerfReview.objects.count() == 3  # One for each team member
        users = User.objects.filter(team_relations__team=team_with_users)
        for user in users:
            assert PerfReview.objects.filter(user=user, team=team_with_users).exists()
    
    def test_perfreview_create_user_as_manager(self, client, manager, user, team_with_users):
        """Test that managers can create reviews for a specific user"""
        client.force_login(manager)
        url = reverse('perfreview_create_user', kwargs={
            'team_id': team_with_users.id,
            'user_id': user.id
        })
        response = client.get(url)
        
        # Should redirect after creating the review
        assert response.status_code == 302
        assert PerfReview.objects.count() == 1
        
        review = PerfReview.objects.first()
        assert review.user == user
        assert review.team == team_with_users
    
    def test_perfreview_create_unauthorized(self, client, user, team):
        """Test that regular users cannot create reviews"""
        client.force_login(user)
        url = reverse('perfreview_create_team', kwargs={'team_id': team.id})
        response = client.get(url)
        
        assert response.status_code == 403  # Forbidden

@pytest.mark.django_db
class TestPerfReviewDetailView:
    
    def test_perfreview_detail_subject(self, client, user, perfreview):
        """Test that the subject user can view their own review"""
        client.force_login(user)
        url = reverse('perfreview_detail', kwargs={'review_id': perfreview.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['review'] == perfreview
        assert response.context['is_subject'] is True
        assert response.context['is_manager'] is False
    
    def test_perfreview_detail_manager(self, client, manager, team_with_users, perfreview):
        """Test that managers can view team members' reviews"""
        client.force_login(manager)
        url = reverse('perfreview_detail', kwargs={'review_id': perfreview.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['review'] == perfreview
        assert response.context['is_subject'] is False
        assert response.context['is_manager'] is True
    
    def test_perfreview_detail_reviewer(self, client, reviewer, achievement_with_reviewer):
        """Test that reviewers can view reviews they are reviewing"""
        client.force_login(reviewer)
        url = reverse('perfreview_detail', kwargs={'review_id': achievement_with_reviewer.perfreview.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['review'] == achievement_with_reviewer.perfreview
        assert response.context['is_subject'] is False
        assert response.context['is_manager'] is False
    
    def test_perfreview_detail_unauthorized(self, client, user, manager, team):
        """Test that unauthorized users cannot view reviews"""
        # Create a new review that the user shouldn't have access to
        other_user = User.objects.create_user(
            email="other@example.com",
            password="password123", 
            user_name="Other User"
        )
        other_review = PerfReview.objects.create(user=other_user, team=team)
        
        client.force_login(user)
        url = reverse('perfreview_detail', kwargs={'review_id': other_review.id})
        response = client.get(url)
        
        assert response.status_code == 403  # Forbidden

@pytest.mark.django_db
class TestAchievementCreateView:
    
    def test_achievement_create_subject(self, client, user, perfreview):
        """Test that subject users can create achievements for their own reviews"""
        client.force_login(user)
        url = reverse('achievement_create', kwargs={'review_id': perfreview.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['review'] == perfreview
        
        # Post data to create achievement
        form_data = {
            'title': 'New Achievement',
            'self_score': 4,
            'reviewers': []
        }
        response = client.post(url, form_data)
        
        assert response.status_code == 302  # Redirect after success
        assert Achievement.objects.count() == 1
        
        achievement = Achievement.objects.first()
        assert achievement.perfreview == perfreview
        assert achievement.title == 'New Achievement'
        assert achievement.self_score == 4
    
    def test_achievement_create_manager(self, client, manager, perfreview, team_with_users):
        """Test that managers can create achievements for team members"""
        client.force_login(manager)
        url = reverse('achievement_create', kwargs={'review_id': perfreview.id})
        
        form_data = {
            'title': 'Manager Added Achievement',
            'self_score': 5,
            'reviewers': []
        }
        response = client.post(url, form_data)
        
        assert response.status_code == 302  # Redirect after success
        assert Achievement.objects.count() == 1
        
        achievement = Achievement.objects.first()
        assert achievement.perfreview == perfreview
        assert achievement.title == 'Manager Added Achievement'
        assert achievement.self_score == 5
    
    def test_achievement_create_unauthorized(self, client, reviewer, perfreview):
        """Test that unauthorized users cannot create achievements"""
        client.force_login(reviewer)
        url = reverse('achievement_create', kwargs={'review_id': perfreview.id})
        response = client.get(url)
        
        assert response.status_code == 403  # Forbidden

@pytest.mark.django_db
class TestAchievementScoreView:
    
    def test_achievement_score_reviewer(self, client, reviewer, achievement_with_reviewer):
        """Test that reviewers can score achievements"""
        client.force_login(reviewer)
        url = reverse('achievement_score', kwargs={'achievement_id': achievement_with_reviewer.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['achievement'] == achievement_with_reviewer
        
        # Post data to score achievement
        form_data = {
            'score': 4,
            'comment': 'Great work!'
        }
        response = client.post(url, form_data)
        
        assert response.status_code == 302  # Redirect after success
        assert AchievementScore.objects.count() == 1
        
        score = AchievementScore.objects.first()
        assert score.achievement == achievement_with_reviewer
        assert score.user == reviewer
        assert score.score == 4
        assert score.comment == 'Great work!'
    
    def test_achievement_score_manager(self, client, manager, achievement_with_reviewer, team_with_users):
        """Test that managers can score achievements even if they are not reviewers"""
        client.force_login(manager)
        url = reverse('achievement_score', kwargs={'achievement_id': achievement_with_reviewer.id})
        
        form_data = {
            'score': 3,
            'comment': 'Good but needs improvement'
        }
        response = client.post(url, form_data)
        
        assert response.status_code == 302  # Redirect after success
        assert AchievementScore.objects.count() == 1
        
        score = AchievementScore.objects.first()
        assert score.achievement == achievement_with_reviewer
        assert score.user == manager
        assert score.score == 3
        assert score.comment == 'Good but needs improvement'
    
    def test_achievement_score_unauthorized(self, client, user, achievement_with_reviewer):
        """Test that unauthorized users cannot score achievements"""
        client.force_login(user)
        url = reverse('achievement_score', kwargs={'achievement_id': achievement_with_reviewer.id})
        response = client.get(url)
        
        assert response.status_code == 403  # Forbidden
    
    def test_achievement_score_update(self, client, reviewer, achievement_score):
        """Test that reviewers can update their scores"""
        client.force_login(reviewer)
        url = reverse('achievement_score', kwargs={'achievement_id': achievement_score.achievement.id})
        
        # Update existing score
        form_data = {
            'score': 5,  # Changed from 4
            'comment': 'Updated comment'
        }
        response = client.post(url, form_data)
        
        assert response.status_code == 302  # Redirect after success
        assert AchievementScore.objects.count() == 1  # Still only one score
        
        # Refresh from DB
        achievement_score.refresh_from_db()
        assert achievement_score.score == 5  # Should be updated
        assert achievement_score.comment == 'Updated comment'  # Should be updated
