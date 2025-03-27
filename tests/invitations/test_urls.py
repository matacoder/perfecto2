import pytest
from django.urls import reverse, resolve
from invitations.views import (
    create_company_invitation, 
    create_team_invitation,
    invitation_accept,
    invitation_list
)

class TestInvitationUrls:
    
    def test_create_company_invitation_url(self):
        """Test URL for creating company invitation"""
        url = reverse('create_company_invitation', kwargs={'company_id': 1})
        assert url == '/invitations/company/1/invite/'
        assert resolve(url).func == create_company_invitation
    
    def test_create_team_invitation_url(self):
        """Test URL for creating team invitation"""
        url = reverse('create_team_invitation', kwargs={'team_id': 1})
        assert url == '/invitations/team/1/invite/'
        assert resolve(url).func == create_team_invitation
    
    def test_invitation_accept_url(self):
        """Test URL for accepting invitation"""
        # Using a dummy UUID
        uuid = '12345678-1234-5678-1234-567812345678'
        url = reverse('invitation_accept', kwargs={'uuid': uuid})
        assert url == f'/invitations/accept/{uuid}/'
        assert resolve(url).func == invitation_accept
    
    def test_invitation_list_url(self):
        """Test URL for invitation list"""
        url = reverse('invitation_list')
        assert url == '/invitations/my-invitations/'
        assert resolve(url).func == invitation_list
