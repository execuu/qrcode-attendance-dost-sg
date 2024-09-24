from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def createUser(self, email, studentNumber=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, studentNumber=studentNumber, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def createSuperUser(self, email, studentNumber=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.createUser(email, studentNumber, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    studentNumber = models.PositiveIntegerField(unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['studentNumber']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        related_name='custom_users_groups',  # Updated related_name for groups
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users_permissions',  # Updated related_name for permissions
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.email
