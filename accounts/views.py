from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
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
    # Check if there's a pending invitation
    pending_invitation_id = request.session.get('pending_invitation')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Process invitation if it exists
            if pending_invitation_id:
                try:
                    from invitations.models import Invitation
                    invitation = Invitation.objects.get(id=pending_invitation_id)
                    
                    # Add user to company or team based on invitation type
                    if invitation.invitation_type == Invitation.TYPE_COMPANY:
                        from companies.models import CompanyUsers
                        CompanyUsers.objects.create(
                            user=user,
                            company=invitation.company,
                            is_manager=invitation.is_manager_invite,
                            is_owner=False
                        )
                        messages.success(request, f"Вы успешно присоединились к компании {invitation.company.company_name}!")
                        
                        # Clear the pending invitation
                        del request.session['pending_invitation']
                        return redirect('company_detail', company_id=invitation.company.id)
                    
                    else:  # Team invitation
                        from companies.models import CompanyUsers
                        from teams.models import TeamUsers
                        
                        # First add user to company
                        CompanyUsers.objects.create(
                            user=user,
                            company=invitation.company,
                            is_manager=False,
                            is_owner=False
                        )
                        
                        # Then add to team
                        TeamUsers.objects.create(
                            user=user,
                            team=invitation.team,
                            is_manager=invitation.is_manager_invite,
                            is_owner=False
                        )
                        
                        messages.success(request, f"Вы успешно присоединились к команде {invitation.team.team_name}!")
                        
                        # Clear the pending invitation
                        del request.session['pending_invitation']
                        return redirect('team_detail', team_id=invitation.team.id)
                        
                except Exception as e:
                    messages.error(request, f"Возникла ошибка при обработке приглашения: {str(e)}")
            
            # No invitation or error processing invitation
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    # If there's a pending invitation, show that in the template context
    invitation_info = None
    if pending_invitation_id:
        try:
            from invitations.models import Invitation
            invitation = Invitation.objects.get(id=pending_invitation_id)
            if not invitation.is_expired:
                invitation_info = {
                    'type': 'команду' if invitation.invitation_type == Invitation.TYPE_TEAM else 'компанию',
                    'name': invitation.target_name
                }
        except Exception:
            pass
    
    return render(request, 'accounts/register.html', {
        'form': form,
        'invitation_info': invitation_info
    })

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
