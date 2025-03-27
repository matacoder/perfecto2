from django import forms
from .models import Team
from accounts.models import User
from companies.models import CompanyUsers

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'team_description']
        widgets = {
            'team_description': forms.Textarea(attrs={'rows': 4}),
        }

class TeamUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=None)
    is_manager = forms.BooleanField(required=False, initial=False)
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(TeamUserForm, self).__init__(*args, **kwargs)
        
        if company:
            # Only show users that are part of the company
            company_user_ids = CompanyUsers.objects.filter(company=company).values_list('user_id', flat=True)
            self.fields['user'].queryset = User.objects.filter(id__in=company_user_ids)
        else:
            self.fields['user'].queryset = User.objects.none()
