from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        #1. Check if email is provided
        if not email:
            raise ValueError("Email must be provided")
        #2. Normalize email
        email = self.normalize_email(email)
        #3. Create user instance
        user = self.model(email=email, **extra_fields)
        #4. Hash password
        user.set_password(password)
        #5. Save user
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        #Setting fields for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        #Validation for superuser fields
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser is not staff")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser is not superuser")
        return self.create_user(email, password, **extra_fields)
class User(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=30, unique=True)
    name=models.CharField(max_length=50, blank=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    following=models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    def __str__(self):
        return self.username
    