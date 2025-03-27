from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TelegramLoginForm
from .models import User
import uuid
import jwt
from django.conf import settings
import datetime

def home_view(request):
    """Home page view showcasing the product description."""
    return render(request, 'accounts/home.html')

def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Login view for traditional email/password authentication."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Form uses username but we store in email
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    
    telegram_form = TelegramLoginForm()
    return render(request, 'accounts/login.html', {
        'form': form,
        'telegram_form': telegram_form
    })

def telegram_login_request(request):
    """Generate one-time link for Telegram authentication."""
    if request.method == 'POST':
        form = TelegramLoginForm(request.POST)
        if form.is_valid():
            telegram_username = form.cleaned_data['telegram_username']
            # Generate one-time token
            token = str(uuid.uuid4())
            # TODO: Implement actual Telegram bot integration
            # For MVP, we'll just redirect with a success message
            return render(request, 'accounts/telegram_link_sent.html', {
                'telegram_username': telegram_username
            })
    
    return redirect('login')

@login_required
def dashboard_view(request):
    """Main dashboard view after login."""
    return render(request, 'accounts/dashboard.html')
