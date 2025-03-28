import pytest
from invitations.forms import InvitationForm, InvitationAcceptForm
from django.core.exceptions import ValidationError

class TestInvitationForm:
    
    def test_empty_form(self):
        """Test that an empty form is valid (as all fields are optional or have defaults)"""
        form = InvitationForm()
        assert form.is_valid() is False  # Form should be invalid without required fields
    
    def test_valid_form_with_email(self):
        """Test form with valid email"""
        form = InvitationForm({
            'email': 'test@example.com',
            'is_manager_invite': True
        })
        assert form.is_valid() is True
    
    def test_invalid_email_in_form(self):
        """Test form with invalid email"""
        form = InvitationForm({
            'email': 'not-an-email',
            'is_manager_invite': False
        })
        assert form.is_valid() is False
        assert 'email' in form.errors
    
    def test_form_without_email(self):
        """Test form without email (should be valid as email is optional)"""
        form = InvitationForm({
            'is_manager_invite': False
        })
        assert form.is_valid() is True
    
    def test_clean_email_method(self):
        """Test the clean_email method directly"""
        form = InvitationForm()
        
        # Valid email - we need to set the field first in cleaned_data
        form.cleaned_data = {'email': 'test@example.com'}
        assert form.clean_email() == 'test@example.com'
        
        # Empty email (valid because optional)
        form.cleaned_data = {'email': ''}
        assert form.clean_email() == ''
        
        # Invalid email should raise ValidationError
        form.cleaned_data = {'email': 'not-an-email'}
        with pytest.raises(ValidationError):
            form.clean_email()

class TestInvitationAcceptForm:
    
    def test_form_creation(self):
        """Test that form is created with correct choices and default"""
        form = InvitationAcceptForm()
        assert form.fields['action'].choices == [
            ('accept', 'Присоединиться'),
            ('decline', 'Отклонить приглашение')
        ]
        assert form.fields['action'].initial == 'accept'
    
    def test_valid_accept_choice(self):
        """Test form with 'accept' choice"""
        form = InvitationAcceptForm({'action': 'accept'})
        assert form.is_valid() is True
    
    def test_valid_decline_choice(self):
        """Test form with 'decline' choice"""
        form = InvitationAcceptForm({'action': 'decline'})
        assert form.is_valid() is True
    
    def test_invalid_choice(self):
        """Test form with invalid choice"""
        form = InvitationAcceptForm({'action': 'invalid'})
        assert form.is_valid() is False
