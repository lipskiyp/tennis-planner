'''
Custom user model.
'''
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()  # assign model manager

    USERNAME_FIELD = "email"  # use an email address as the primary user identifier
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
