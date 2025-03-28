from django import forms
from .models import Invitation
from accounts.models import User
from django.core.validators import validate_email

class InvitationForm(forms.ModelForm):
    """Form for creating new invitations."""
    email = forms.EmailField(required=False, help_text="Необязательно: укажите email для приглашения конкретного пользователя")
    
    class Meta:
        model = Invitation
        fields = ['email', 'is_manager_invite']
        
    def clean_email(self):
        """Validate the email field."""
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except forms.ValidationError:
                raise forms.ValidationError("Пожалуйста, введите корректный email адрес")
        return email

class InvitationAcceptForm(forms.Form):
    """Form shown when accepting an invitation."""
    action = forms.ChoiceField(
        choices=[
            ('accept', 'Присоединиться'),
            ('decline', 'Отклонить приглашение')
        ],
        widget=forms.RadioSelect,
        initial='accept'
    )
