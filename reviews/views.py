from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import PerfReview, Achievement, AchievementScore
from .forms import PerfReviewForm, AchievementForm, AchievementScoreForm
from teams.models import Team, TeamUsers
from companies.models import CompanyUsers
from accounts.models import User

@login_required
def perfreview_list(request):
    """Display performance reviews."""
    # Мои перфревью
    my_reviews = PerfReview.objects.filter(user=request.user)
    
    # Перфревью на оценку (где я ревьюер)
    managed_reviews = PerfReview.objects.filter(
        achievements__reviewers=request.user
    ).distinct().exclude(user=request.user)
    
    # Перфревью команды (где я менеджер или владелец)
    # Было: teams_managed = Team.objects.filter(teamusers__user=request.user, teamusers__is_manager=True)
    # Заменяем на:
    teams_managed = Team.objects.filter(team_users__user=request.user, team_users__is_manager=True)
    
    team_reviews = PerfReview.objects.filter(
        team__in=teams_managed
    ).exclude(user=request.user)
    
    context = {
        'my_reviews': my_reviews,
        'managed_reviews': managed_reviews,
        'team_reviews': team_reviews,
    }
    
    return render(request, 'reviews/perfreview_list.html', context)

@login_required
def perfreviews_create(request, team_id=None, user_id=None):
    """Create a new performance review."""
    # Check if this is for a team or an individual
    if team_id and not user_id:
        # Team review
        team = get_object_or_404(Team, id=team_id)
        # Check permissions
        try:
            team_user = TeamUsers.objects.get(user=request.user, team=team)
            if not team_user.is_manager and not team_user.is_owner:
                # Check if user is company manager
                company_user = CompanyUsers.objects.get(user=request.user, company=team.company)
                if not company_user.is_manager and not company_user.is_owner:
                    return HttpResponseForbidden("You don't have permission to create reviews for this team")
        except (TeamUsers.DoesNotExist, CompanyUsers.DoesNotExist):
            return HttpResponseForbidden("You don't have permission to create reviews for this team")
        
        # Create reviews for all team members
        # Было: team_members = User.objects.filter(teamusers__team=team)
        # Заменяем на:
        team_members = User.objects.filter(team_relations__team=team)
        
        for member in team_members:
            PerfReview.objects.create(user=member, team=team)
        
        return redirect('team_detail', team_id=team.id)
    
    elif user_id and team_id:
        # Individual review
        user = get_object_or_404(User, id=user_id)
        team = get_object_or_404(Team, id=team_id)
        
        # Check permissions
        has_permission = False
        try:
            # Check if requester is team manager
            team_user = TeamUsers.objects.get(user=request.user, team=team)
            has_permission = team_user.is_manager or team_user.is_owner
        except TeamUsers.DoesNotExist:
            pass
        
        if not has_permission:
            try:
                # Check if requester is company manager
                company_user = CompanyUsers.objects.get(user=request.user, company=team.company)
                has_permission = company_user.is_manager or company_user.is_owner
            except CompanyUsers.DoesNotExist:
                pass
        
        if not has_permission:
            return HttpResponseForbidden("You don't have permission to create reviews")
        
        # Create the review
        review = PerfReview.objects.create(user=user, team=team)
        return redirect('perfreview_detail', review_id=review.id)
    
    else:
        return redirect('dashboard')

@login_required
def perfreview_detail(request, review_id):
    """View a specific performance review."""
    review = get_object_or_404(PerfReview, id=review_id)
    achievements = Achievement.objects.filter(perfreview=review)
    
    # Check permissions
    is_subject = review.user == request.user
    
    is_manager = False
    try:
        team_user = TeamUsers.objects.get(user=request.user, team=review.team)
        is_manager = team_user.is_manager or team_user.is_owner
    except TeamUsers.DoesNotExist:
        try:
            company_user = CompanyUsers.objects.get(user=request.user, company=review.team.company)
            is_manager = company_user.is_manager or company_user.is_owner
        except CompanyUsers.DoesNotExist:
            pass
    
    is_reviewer = Achievement.objects.filter(perfreview=review, reviewers=request.user).exists()
    
    # Create a dictionary to track which achievements the user has already scored
    user_scored_achievements = {}
    if is_reviewer:
        # Get all scores by this user for achievements in this review
        from django.db.models import Q
        user_scores = AchievementScore.objects.filter(
            achievement__perfreview=review,
            user=request.user
        ).values_list('achievement_id', flat=True)
        
        # Create a dictionary where keys are achievement IDs and values are True if scored
        for achievement in achievements:
            user_scored_achievements[achievement.id] = achievement.id in user_scores
    
    if not (is_subject or is_manager or is_reviewer):
        return HttpResponseForbidden("You don't have permission to view this review")
    
    context = {
        'review': review,
        'achievements': achievements,
        'is_subject': is_subject,
        'is_manager': is_manager,
        'user_scored_achievements': user_scored_achievements
    }
    
    return render(request, 'reviews/perfreview_detail.html', context)

@login_required
def achievement_create(request, review_id):
    """Create a new achievement for a performance review."""
    review = get_object_or_404(PerfReview, id=review_id)
    
    # Check permissions
    is_subject = review.user == request.user
    is_manager = False
    try:
        team_user = TeamUsers.objects.get(user=request.user, team=review.team)
        is_manager = team_user.is_manager or team_user.is_owner
    except TeamUsers.DoesNotExist:
        try:
            company_user = CompanyUsers.objects.get(user=request.user, company=review.team.company)
            is_manager = company_user.is_manager or company_user.is_owner
        except CompanyUsers.DoesNotExist:
            pass
    
    if not (is_subject or is_manager):
        return HttpResponseForbidden("You don't have permission to add achievements to this review")
    
    if request.method == 'POST':
        form = AchievementForm(request.POST, team=review.team)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.perfreview = review
            achievement.save()
            
            # Add reviewers
            if form.cleaned_data.get('reviewers'):
                achievement.reviewers.set(form.cleaned_data.get('reviewers'))
            
            return redirect('perfreview_detail', review_id=review.id)
    else:
        form = AchievementForm(team=review.team)
    
    return render(request, 'reviews/achievement_form.html', {
        'form': form,
        'review': review
    })

@login_required
def achievement_score(request, achievement_id):
    """Score an achievement as a reviewer."""
    achievement = get_object_or_404(Achievement, id=achievement_id)
    
    # Check permissions
    if request.user not in achievement.reviewers.all():
        is_manager = False
        try:
            team_user = TeamUsers.objects.get(user=request.user, team=achievement.perfreview.team)
            is_manager = team_user.is_manager or team_user.is_owner
        except TeamUsers.DoesNotExist:
            try:
                company_user = CompanyUsers.objects.get(user=request.user, 
                                                      company=achievement.perfreview.team.company)
                is_manager = company_user.is_manager or company_user.is_owner
            except CompanyUsers.DoesNotExist:
                pass
        
        if not is_manager:
            return HttpResponseForbidden("You are not a reviewer for this achievement")
    
    # Check if user already scored this achievement
    try:
        score = AchievementScore.objects.get(achievement=achievement, user=request.user)
    except AchievementScore.DoesNotExist:
        score = None
    
    if request.method == 'POST':
        form = AchievementScoreForm(request.POST, instance=score)
        if form.is_valid():
            new_score = form.save(commit=False)
            new_score.achievement = achievement
            new_score.user = request.user
            new_score.save()
            return redirect('perfreview_detail', review_id=achievement.perfreview.id)
    else:
        form = AchievementScoreForm(instance=score)
    
    return render(request, 'reviews/achievement_score_form.html', {
        'form': form,
        'achievement': achievement
    })
