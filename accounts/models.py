from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Custom user manager that uses email as the unique identifier."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Custom user model that uses email as the primary identifier."""
    
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=255)
    user_job = models.CharField(max_length=255, blank=True)
    telegram_username = models.CharField(max_length=255, blank=True)
    telegram_id = models.CharField(max_length=255, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    @property
    def companies(self):
        """Компании, в которых состоит пользователь."""
        return self.company_relations.all()
    
    @property
    def teams(self):
        """Команды, в которых состоит пользователь."""
        return self.team_relations.all()
    
    @property
    def reviews(self):
        """Перфревью пользователя."""
        return self.perfreview_set.all()
    
    @property
    def invitations(self):
        """Приглашения, созданные пользователем."""
        return self.sent_invitations.all()
