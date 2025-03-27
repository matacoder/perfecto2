from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models import Invitation
from .forms import InvitationForm, InvitationAcceptForm
from companies.models import Company, CompanyUsers
from teams.models import Team, TeamUsers

@login_required
def create_company_invitation(request, company_id):
    """Create an invitation to join a company."""
    company = get_object_or_404(Company, id=company_id)
    
    # Check if user has permission
    try:
        company_user = CompanyUsers.objects.get(user=request.user, company=company)
        if not company_user.is_manager and not company_user.is_owner:
            return HttpResponseForbidden("У вас нет прав для приглашения пользователей в эту компанию")
    except CompanyUsers.DoesNotExist:
        return HttpResponseForbidden("У вас нет доступа к этой компании")
    
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.created_by = request.user
            invitation.invitation_type = Invitation.TYPE_COMPANY
            invitation.company = company
            invitation.save()
            
            invite_url = request.build_absolute_uri(
                reverse('invitation_accept', kwargs={'uuid': invitation.id})
            )
            
            messages.success(
                request, 
                f"Приглашение создано! Ссылка для приглашения: {invite_url}"
            )
            
            return redirect('company_detail', company_id=company.id)
    else:
        form = InvitationForm()
    
    return render(request, 'invitations/create_invitation.html', {
        'form': form,
        'company': company,
        'invitation_type': 'компанию'
    })

@login_required
def create_team_invitation(request, team_id):
    """Create an invitation to join a team."""
    team = get_object_or_404(Team, id=team_id)
    company = team.company
    
    # Check if user has permission (team manager, team owner, company manager, or company owner)
    has_permission = False
    try:
        team_user = TeamUsers.objects.get(user=request.user, team=team)
        has_permission = team_user.is_manager or team_user.is_owner
    except TeamUsers.DoesNotExist:
        try:
            company_user = CompanyUsers.objects.get(user=request.user, company=company)
            has_permission = company_user.is_manager or company_user.is_owner
        except CompanyUsers.DoesNotExist:
            pass
    
    if not has_permission:
        return HttpResponseForbidden("У вас нет прав для приглашения пользователей в эту команду")
    
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.created_by = request.user
            invitation.invitation_type = Invitation.TYPE_TEAM
            invitation.company = company
            invitation.team = team
            invitation.save()
            
            invite_url = request.build_absolute_uri(
                reverse('invitation_accept', kwargs={'uuid': invitation.id})
            )
            
            messages.success(
                request, 
                f"Приглашение создано! Ссылка для приглашения: {invite_url}"
            )
            
            return redirect('team_detail', team_id=team.id)
    else:
        form = InvitationForm()
    
    return render(request, 'invitations/create_invitation.html', {
        'form': form,
        'team': team,
        'company': company,
        'invitation_type': 'команду'
    })

def invitation_accept(request, uuid):
    """Handle invitation acceptance."""
    invitation = get_object_or_404(Invitation, id=uuid)
    
    # Check if invitation has expired
    if invitation.is_expired:
        return render(request, 'invitations/invitation_expired.html', {
            'invitation': invitation
        })
    
    # If user is logged in
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = InvitationAcceptForm(request.POST)
            if form.is_valid():
                action = form.cleaned_data['action']
                if action == 'accept':
                    # Add user to company or team
                    if invitation.invitation_type == Invitation.TYPE_COMPANY:
                        CompanyUsers.objects.get_or_create(
                            user=request.user,
                            company=invitation.company,
                            defaults={
                                'is_manager': invitation.is_manager_invite,
                                'is_owner': False
                            }
                        )
                        messages.success(request, f"Вы присоединились к компании {invitation.company.company_name}!")
                        return redirect('company_detail', company_id=invitation.company.id)
                    
                    else:  # Team invitation
                        # First make sure user is in company
                        CompanyUsers.objects.get_or_create(
                            user=request.user,
                            company=invitation.company,
                            defaults={
                                'is_manager': False,
                                'is_owner': False
                            }
                        )
                        
                        # Then add to team
                        TeamUsers.objects.get_or_create(
                            user=request.user,
                            team=invitation.team,
                            defaults={
                                'is_manager': invitation.is_manager_invite,
                                'is_owner': False
                            }
                        )
                        messages.success(request, f"Вы присоединились к команде {invitation.team.team_name}!")
                        return redirect('team_detail', team_id=invitation.team.id)
                else:  # Declined
                    messages.info(request, "Вы отклонили приглашение.")
                    return redirect('dashboard')
        else:
            form = InvitationAcceptForm()
            
        return render(request, 'invitations/invitation_accept.html', {
            'invitation': invitation,
            'form': form
        })
    
    # If user is not logged in, store invitation ID in session and redirect to register
    else:
        request.session['pending_invitation'] = str(invitation.id)
        return redirect('register')

@login_required
def invitation_list(request):
    """Show list of invitations created by the user."""
    invitations = Invitation.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Filter out expired invitations
    active_invitations = [inv for inv in invitations if not inv.is_expired]
    expired_invitations = [inv for inv in invitations if inv.is_expired]
    
    return render(request, 'invitations/invitation_list.html', {
        'active_invitations': active_invitations,
        'expired_invitations': expired_invitations
    })
