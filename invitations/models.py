from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from accounts.models import User
from companies.models import Company
from teams.models import Team

class Invitation(models.Model):
    """Model for tracking invitations to companies and teams."""
    
    # Types of invitations
    TYPE_COMPANY = 'company'
    TYPE_TEAM = 'team'
    INVITATION_TYPES = [
        (TYPE_COMPANY, 'Company'),
        (TYPE_TEAM, 'Team'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    invitation_type = models.CharField(max_length=10, choices=INVITATION_TYPES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invitations')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='invitations')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_manager_invite = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)  # Optional: specific email for invitation
    
    def save(self, *args, **kwargs):
        # Set expiration date to 7 days from now if not specified
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        """Check if the invitation has expired."""
        return timezone.now() > self.expires_at
    
    @property
    def target_name(self):
        """Return name of the company or team for this invitation."""
        if self.invitation_type == self.TYPE_TEAM and self.team:
            return self.team.team_name
        return self.company.company_name
    
    def get_absolute_url(self):
        """Return the URL to accept this invitation."""
        return reverse('invitation_accept', kwargs={'uuid': str(self.id)})
    
    def __str__(self):
        if self.invitation_type == self.TYPE_TEAM:
            return f"Invitation to {self.team.team_name} team"
        return f"Invitation to {self.company.company_name} company"
