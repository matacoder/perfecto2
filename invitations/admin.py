from django.contrib import admin
from .models import Invitation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'invitation_type', 'target_name', 'created_by', 'created_at', 'expires_at', 'is_expired')
    list_filter = ('invitation_type', 'is_manager_invite', 'created_at')
    search_fields = ('created_by__email', 'company__company_name', 'team__team_name')
    readonly_fields = ('id', 'created_at')
    date_hierarchy = 'created_at'
    
    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
    
    def target_name(self, obj):
        return obj.target_name
    target_name.short_description = 'Target'
