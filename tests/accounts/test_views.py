import pytest
from django.urls import reverse
from accounts.models import User
import uuid

@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com",
        password="password123",
        user_name="Test User"
    )

@pytest.mark.django_db
class TestHomeView:
    
    def test_home_view(self, client):
        """Test that home view can be accessed by anyone"""
        url = reverse('home')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'accounts/home.html' in [t.name for t in response.templates]

@pytest.mark.django_db
class TestRegisterView:
    
    def test_register_view_get(self, client):
        """Test GET request to register view"""
        url = reverse('register')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'accounts/register.html' in [t.name for t in response.templates]
    
    def test_register_view_post_success(self, client):
        """Test successful user registration"""
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'user_name': 'New User',
            'user_job': 'Developer',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        }
        response = client.post(url, data)
        
        assert response.status_code == 302  # Redirect after successful registration
        assert User.objects.filter(email='newuser@example.com').exists()
        
        # Check if user is automatically logged in
        # The response should redirect to dashboard
        assert response.url == reverse('dashboard')
    
    def test_register_view_post_invalid(self, client):
        """Test registration with invalid data"""
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'user_name': 'New User',
            'password1': 'password123',
            'password2': 'different_password'  # Passwords don't match
        }
        response = client.post(url, data)
        
        assert response.status_code == 200  # Stay on the same page
        assert not User.objects.filter(email='newuser@example.com').exists()
        assert 'form' in response.context
        assert response.context['form'].errors
    
    def test_register_with_invitation(self, client):
        """Test registration with a pending invitation"""
        # Store a fake invitation UUID in the session
        session = client.session
        session['pending_invitation'] = str(uuid.uuid4())
        session.save()
        
        url = reverse('register')
        response = client.get(url)
        
        # Check if the invitation info is in the context
        # This might be None since we're using a fake UUID
        assert 'invitation_info' in response.context

@pytest.mark.django_db
class TestLoginView:
    
    def test_login_view_get(self, client):
        """Test GET request to login view"""
        url = reverse('login')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'telegram_form' in response.context
        assert 'accounts/login.html' in [t.name for t in response.templates]
    
    def test_login_view_post_success(self, client, user):
        """Test successful login"""
        url = reverse('login')
        data = {
            'username': 'test@example.com',
            'password': 'password123'
        }
        response = client.post(url, data)
        
        assert response.status_code == 302  # Redirect after successful login
        assert response.url == reverse('dashboard')
    
    def test_login_view_post_invalid(self, client):
        """Test login with invalid credentials"""
        url = reverse('login')
        data = {
            'username': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = client.post(url, data)
        
        assert response.status_code == 200  # Stay on the same page
        assert 'form' in response.context
        assert response.context['form'].errors

@pytest.mark.django_db
class TestDashboardView:
    
    def test_dashboard_authenticated(self, client, user):
        """Test that authenticated users can access dashboard"""
        client.force_login(user)
        url = reverse('dashboard')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'accounts/dashboard.html' in [t.name for t in response.templates]
    
    def test_dashboard_unauthenticated(self, client):
        """Test that unauthenticated users are redirected to login"""
        url = reverse('dashboard')
        response = client.get(url)
        
        assert response.status_code == 302
        assert '/accounts/login/' in response.url

@pytest.mark.django_db
class TestTelegramLoginRequestView:
    
    def test_telegram_login_request_post(self, client):
        """Test POST request to telegram login request view"""
        # Fix: Use the correct URL name
        url = reverse('telegram_login')
        data = {
            'telegram_username': '@testuser'
        }
        response = client.post(url, data)
        
        # For now, this should show the telegram link sent template
        # or redirect to login page
        assert response.status_code in [200, 302]
        
        if response.status_code == 200:
            assert 'accounts/telegram_link_sent.html' in [t.name for t in response.templates]
    
    def test_telegram_login_request_get(self, client):
        """Test GET request to telegram login request view should redirect to login"""
        # Fix: Use the correct URL name
        url = reverse('telegram_login')
        response = client.get(url)
        
        assert response.status_code == 302
        assert response.url == reverse('login')
