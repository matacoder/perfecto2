from django.db import models
from accounts.models import User
from teams.models import Team

class PerfReview(models.Model):
    """Performance review model for tracking user reviews in teams."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='perfreview_set')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Performance Reviews'
        unique_together = ('user', 'team', 'created')
    
    def __str__(self):
        return f"Review for {self.user.user_name} in {self.team.team_name}"

class Achievement(models.Model):
    """Achievement within a performance review."""
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    perfreview = models.ForeignKey(PerfReview, on_delete=models.CASCADE, related_name='achievements')
    title = models.TextField()
    self_score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    reviewers = models.ManyToManyField(User, related_name='reviewing_achievements')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title[:50]}..."

class AchievementScore(models.Model):
    """Scores given by reviewers to achievements."""
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='scores')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_scores')
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('achievement', 'user')
    
    def __str__(self):
        return f"Score for {self.achievement} by {self.user.user_name}"
