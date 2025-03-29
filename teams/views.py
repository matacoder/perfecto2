from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from .models import Team, TeamUsers
from .forms import TeamForm, TeamUserForm
from companies.models import Company, CompanyUsers

@login_required
def team_list(request):
    """Display teams where the user is a member."""
    user_teams = Team.objects.filter(team_users__user=request.user)
    return render(request, 'teams/team_list.html', {'teams': user_teams})

@login_required
def team_create(request, company_id):
    """Create a new team within a company."""
    company = get_object_or_404(Company, id=company_id)
    
    # Check if user is manager or owner of the company
    try:
        user_company = CompanyUsers.objects.get(user=request.user, company=company)
        if not (user_company.is_manager or user_company.is_owner):
            return HttpResponseForbidden("You don't have permissions to create teams in this company")
    except CompanyUsers.DoesNotExist:
        return HttpResponseForbidden("You don't have access to this company")
    
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.company = company
            team.save()
            
            # Make the creator both owner and manager of the team
            TeamUsers.objects.create(
                user=request.user,
                team=team,
                is_manager=True,
                is_owner=True
            )
            return redirect('team_detail', team_id=team.id)
    else:
        form = TeamForm()
    
    return render(request, 'teams/team_form.html', {
        'form': form,
        'company': company
    })

@login_required
def team_detail(request, team_id):
    """View team details."""
    team = get_object_or_404(Team, id=team_id)
    
    # Check if user is part of this team or the company
    try:
        user_team = TeamUsers.objects.get(user=request.user, team=team)
        is_team_manager = user_team.is_manager
        is_team_owner = user_team.is_owner
    except TeamUsers.DoesNotExist:
        # Check if user is a company manager/owner
        try:
            user_company = CompanyUsers.objects.get(user=request.user, company=team.company)
            is_team_manager = user_company.is_manager or user_company.is_owner
            is_team_owner = user_company.is_owner
        except CompanyUsers.DoesNotExist:
            return HttpResponseForbidden("You don't have access to this team")
    
    team_users = TeamUsers.objects.filter(team=team)
    
    context = {
        'team': team,
        'company': team.company,
        'team_users': team_users,
        'is_manager': is_team_manager,
        'is_owner': is_team_owner
    }
    
    return render(request, 'teams/team_detail.html', context)

@login_required
def team_add_user(request, team_id):
    """Add a user to a team."""
    team = get_object_or_404(Team, id=team_id)
    
    # Check if current user is a team manager, team owner, or company manager/owner
    has_permission = False
    try:
        user_team = TeamUsers.objects.get(user=request.user, team=team)
        has_permission = user_team.is_manager or user_team.is_owner
    except TeamUsers.DoesNotExist:
        try:
            user_company = CompanyUsers.objects.get(user=request.user, company=team.company)
            has_permission = user_company.is_manager or user_company.is_owner
        except CompanyUsers.DoesNotExist:
            pass
    
    if not has_permission:
        return HttpResponseForbidden("You don't have permission to add users to this team")
    
    if request.method == 'POST':
        form = TeamUserForm(request.POST, company=team.company)
        if form.is_valid():
            new_user = form.cleaned_data['user']
            is_manager = form.cleaned_data['is_manager']
            
            # Check if user is already part of the team
            team_user, created = TeamUsers.objects.get_or_create(
                user=new_user,
                team=team,
                defaults={'is_manager': is_manager, 'is_owner': False}
            )
            
            if not created:
                team_user.is_manager = is_manager
                team_user.save()
            
            return redirect('team_detail', team_id=team.id)
    else:
        form = TeamUserForm(company=team.company)
    
    return render(request, 'teams/team_add_user.html', {
        'form': form,
        'team': team
    })
