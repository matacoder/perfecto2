import pytest
from django.urls import reverse
from accounts.models import User
from companies.models import Company, CompanyUsers

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
def company_with_user(company, user):
    CompanyUsers.objects.create(
        user=user,
        company=company,
        is_manager=True,
        is_owner=True
    )
    return company

@pytest.mark.django_db
class TestCompanyListView:
    
    def test_company_list_view_authenticated(self, client, user, company_with_user):
        """Test that authenticated users can access the company list view"""
        client.force_login(user)
        url = reverse('company_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['companies']) == 1
        assert response.context['companies'][0] == company_with_user
    
    def test_company_list_view_unauthenticated(self, client):
        """Test that unauthenticated users are redirected to login"""
        url = reverse('company_list')
        response = client.get(url)
        
        assert response.status_code == 302
        assert '/accounts/login/' in response.url
    
    def test_company_list_view_no_companies(self, client, user):
        """Test that company list view shows no companies if user has none"""
        client.force_login(user)
        url = reverse('company_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['companies']) == 0

@pytest.mark.django_db
class TestCompanyCreateView:
    
    def test_company_create_view_get(self, client, user):
        """Test that authenticated users can access the company create view"""
        client.force_login(user)
        url = reverse('company_create')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_company_create_view_post(self, client, user):
        """Test that authenticated users can create companies"""
        client.force_login(user)
        url = reverse('company_create')
        data = {
            'company_name': 'New Company',
            'company_description': 'New Company Description'
        }
        response = client.post(url, data)
        
        assert response.status_code == 302
        assert Company.objects.count() == 1
        
        company = Company.objects.first()
        assert company.company_name == 'New Company'
        assert company.company_description == 'New Company Description'
        
        # Check that the user is set as owner and manager
        company_user = CompanyUsers.objects.get(user=user, company=company)
        assert company_user.is_owner is True
        assert company_user.is_manager is True
    
    def test_company_create_view_unauthenticated(self, client):
        """Test that unauthenticated users are redirected to login"""
        url = reverse('company_create')
        response = client.get(url)
        
        assert response.status_code == 302
        assert '/accounts/login/' in response.url

@pytest.mark.django_db
class TestCompanyDetailView:
    
    def test_company_detail_view_owner(self, client, user, company_with_user):
        """Test that company owners can access the company detail view"""
        client.force_login(user)
        url = reverse('company_detail', kwargs={'company_id': company_with_user.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['company'] == company_with_user
        assert response.context['is_owner'] is True
        assert response.context['is_manager'] is True
        assert len(response.context['company_users']) == 1
    
    def test_company_detail_view_unauthenticated(self, client, company):
        """Test that unauthenticated users are redirected to login"""
        url = reverse('company_detail', kwargs={'company_id': company.id})
        response = client.get(url)
        
        assert response.status_code == 302
        assert '/accounts/login/' in response.url
    
    def test_company_detail_view_unauthorized(self, client, another_user, company):
        """Test that unauthorized users get a forbidden response"""
        client.force_login(another_user)
        url = reverse('company_detail', kwargs={'company_id': company.id})
        response = client.get(url)
        
        assert response.status_code == 403

@pytest.mark.django_db
class TestCompanyAddUserView:
    
    def test_company_add_user_view_get(self, client, user, company_with_user):
        """Test that company owners can access the company add user view"""
        client.force_login(user)
        url = reverse('company_add_user', kwargs={'company_id': company_with_user.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['company'] == company_with_user
    
    def test_company_add_user_view_post(self, client, user, another_user, company_with_user):
        """Test that company owners can add users to the company"""
        client.force_login(user)
        url = reverse('company_add_user', kwargs={'company_id': company_with_user.id})
        data = {
            'user': another_user.id,
            'is_manager': True
        }
        response = client.post(url, data)
        
        assert response.status_code == 302
        assert CompanyUsers.objects.filter(company=company_with_user, user=another_user).exists()
        
        company_user = CompanyUsers.objects.get(company=company_with_user, user=another_user)
        assert company_user.is_manager is True
        assert company_user.is_owner is False
    
    def test_company_add_user_view_update_existing(self, client, user, another_user, company_with_user):
        """Test that company owners can update existing users in the company"""
        # Create the user with manager=False first
        CompanyUsers.objects.create(
            user=another_user,
            company=company_with_user,
            is_manager=False,
            is_owner=False
        )
        
        client.force_login(user)
        url = reverse('company_add_user', kwargs={'company_id': company_with_user.id})
        data = {
            'user': another_user.id,
            'is_manager': True
        }
        response = client.post(url, data)
        
        assert response.status_code == 302
        company_user = CompanyUsers.objects.get(company=company_with_user, user=another_user)
        assert company_user.is_manager is True  # Should be updated to True
        
    def test_company_add_user_view_unauthorized(self, client, another_user, company):
        """Test that unauthorized users get a forbidden response"""
        client.force_login(another_user)
        url = reverse('company_add_user', kwargs={'company_id': company.id})
        response = client.get(url)
        
        assert response.status_code == 403
