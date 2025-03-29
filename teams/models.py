from django.db import models
from accounts.models import User
from companies.models import Company

class Team(models.Model):
    """Team model representing teams within companies."""
    team_name = models.CharField(max_length=255)
    team_description = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='teams')
    users = models.ManyToManyField(User, through='TeamUsers', related_name='team_set')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.team_name

class TeamUsers(models.Model):
    """Association table between User and Team models."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_relations')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_users')
    is_manager = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Team Users'
        unique_together = ('user', 'team')
    
    def __str__(self):
        return f"{self.user.email} - {self.team.team_name}"
