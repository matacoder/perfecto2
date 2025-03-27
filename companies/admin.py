from django.contrib import admin
from .models import Company, CompanyUsers

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'created')
    search_fields = ('company_name', 'company_description')
    date_hierarchy = 'created'

@admin.register(CompanyUsers)
class CompanyUsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'is_manager', 'is_owner')
    list_filter = ('is_manager', 'is_owner')
    search_fields = ('user__email', 'company__company_name')
