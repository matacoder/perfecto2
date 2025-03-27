#!/usr/bin/env python
"""
Setup script to initialize the Perfecto application.
This creates a superuser and sets up initial data for testing.
"""
import os
import sys
import django
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "perfecto.settings")
django.setup()

from accounts.models import User
from companies.models import Company, CompanyUsers
from teams.models import Team, TeamUsers

def setup_database():
    """Run migrations and create initial data."""
    print("Running migrations...")
    call_command('makemigrations', 'accounts', 'companies', 'teams', 'reviews', 'invitations')
    call_command('migrate')
    
    # Create a superuser for admin access
    if not User.objects.filter(email='admin@example.com').exists():
        print("Creating superuser...")
        User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            user_name='Admin User'
        )
    
    # Create a regular user for testing
    if not User.objects.filter(email='user@example.com').exists():
        print("Creating test user...")
        user = User.objects.create_user(
            email='user@example.com',
            password='userpassword',
            user_name='Test User',
            user_job='Software Developer'
        )
        
        # Create a test company and add the user as owner
        company = Company.objects.create(
            company_name='Test Company',
            company_description='A company for testing purposes'
        )
        CompanyUsers.objects.create(
            user=user,
            company=company,
            is_manager=True,
            is_owner=True
        )
        
        # Create a test team and add the user
        team = Team.objects.create(
            team_name='Test Team',
            team_description='A team for testing purposes',
            company=company
        )
        TeamUsers.objects.create(
            user=user,
            team=team,
            is_manager=True,
            is_owner=True
        )
    
    print("Setup complete!")

if __name__ == "__main__":
    setup_database()
