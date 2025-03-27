from django.contrib import admin
from .models import Team, TeamUsers

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'company', 'created')
    list_filter = ('company',)
    search_fields = ('team_name', 'team_description', 'company__company_name')
    date_hierarchy = 'created'

@admin.register(TeamUsers)
class TeamUsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'is_manager', 'is_owner')
    list_filter = ('is_manager', 'is_owner', 'team')
    search_fields = ('user__email', 'team__team_name')
