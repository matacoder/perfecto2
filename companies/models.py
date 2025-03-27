from django.db import models
from accounts.models import User

class Company(models.Model):
    """Company model representing organizations in the system."""
    company_name = models.CharField(max_length=255)
    company_description = models.TextField(blank=True)
    users = models.ManyToManyField(User, through='CompanyUsers')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return self.company_name

class CompanyUsers(models.Model):
    """Association table between User and Company models."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Company Users'
        unique_together = ('user', 'company')
    
    def __str__(self):
        return f"{self.user.email} - {self.company.company_name}"
