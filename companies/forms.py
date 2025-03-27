from django import forms
from .models import Company
from accounts.models import User

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_description']
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4}),
        }

class CompanyUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    is_manager = forms.BooleanField(required=False, initial=False)
