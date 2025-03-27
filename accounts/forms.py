from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_name = forms.CharField(max_length=255, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'user_name', 'user_job', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Set username to email for compatibility
        user.user_name = self.cleaned_data['user_name']
        user.user_job = self.cleaned_data.get('user_job', '')
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
    
    class Meta:
        model = User
        fields = ('username', 'password')

class TelegramLoginForm(forms.Form):
    telegram_username = forms.CharField(max_length=255, required=True)
