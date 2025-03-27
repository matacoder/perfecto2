from django import forms
from .models import PerfReview, Achievement, AchievementScore
from accounts.models import User
from companies.models import CompanyUsers

class PerfReviewForm(forms.ModelForm):
    class Meta:
        model = PerfReview
        fields = []  # No editable fields, just creation

class AchievementForm(forms.ModelForm):
    reviewers = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Achievement
        fields = ['title', 'self_score', 'reviewers']
    
    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super(AchievementForm, self).__init__(*args, **kwargs)
        
        if team:
            # Only show reviewers from the same company
            company = team.company
            company_users = CompanyUsers.objects.filter(company=company).values_list('user_id', flat=True)
            self.fields['reviewers'].queryset = User.objects.filter(id__in=company_users)
        else:
            self.fields['reviewers'].queryset = User.objects.none()

class AchievementScoreForm(forms.ModelForm):
    class Meta:
        model = AchievementScore
        fields = ['score', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
