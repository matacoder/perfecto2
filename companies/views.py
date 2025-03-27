from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Company, CompanyUsers
from .forms import CompanyForm, CompanyUserForm

@login_required
def company_list(request):
    """Display companies where the user is a member."""
    user_companies = Company.objects.filter(companyusers__user=request.user)
    return render(request, 'companies/company_list.html', {'companies': user_companies})

@login_required
def company_create(request):
    """Create a new company."""
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            # Make the creator both owner and manager
            CompanyUsers.objects.create(
                user=request.user,
                company=company,
                is_manager=True,
                is_owner=True
            )
            return redirect('company_detail', company_id=company.id)
    else:
        form = CompanyForm()
    
    return render(request, 'companies/company_form.html', {'form': form})

@login_required
def company_detail(request, company_id):
    """View company details."""
    company = get_object_or_404(Company, id=company_id)
    
    # Check if user is part of this company
    try:
        user_role = CompanyUsers.objects.get(user=request.user, company=company)
        is_manager = user_role.is_manager
        is_owner = user_role.is_owner
    except CompanyUsers.DoesNotExist:
        return HttpResponseForbidden("You don't have access to this company")
    
    company_users = CompanyUsers.objects.filter(company=company)
    
    context = {
        'company': company,
        'company_users': company_users,
        'is_manager': is_manager,
        'is_owner': is_owner
    }
    
    return render(request, 'companies/company_detail.html', context)

@login_required
def company_add_user(request, company_id):
    """Add a user to a company."""
    company = get_object_or_404(Company, id=company_id)
    
    # Verify the current user is a manager or owner
    try:
        user_role = CompanyUsers.objects.get(user=request.user, company=company)
        if not (user_role.is_manager or user_role.is_owner):
            return HttpResponseForbidden("You don't have permissions to add users to this company")
    except CompanyUsers.DoesNotExist:
        return HttpResponseForbidden("You don't have access to this company")
    
    if request.method == 'POST':
        form = CompanyUserForm(request.POST)
        if form.is_valid():
            new_user = form.cleaned_data['user']
            is_manager = form.cleaned_data['is_manager']
            
            # Check if the user already exists in the company
            company_user, created = CompanyUsers.objects.get_or_create(
                user=new_user,
                company=company,
                defaults={'is_manager': is_manager, 'is_owner': False}
            )
            
            if not created:
                company_user.is_manager = is_manager
                company_user.save()
            
            return redirect('company_detail', company_id=company.id)
    else:
        form = CompanyUserForm()
    
    return render(request, 'companies/company_add_user.html', {
        'form': form,
        'company': company
    })
