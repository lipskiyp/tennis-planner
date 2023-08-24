'''
Custom user manager.
'''
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for database query operations.
    https://docs.djangoproject.com/en/4.1/topics/db/managers/
    """
    def create_user(self, email, password=None, **extra_fields):  # password=None allows unusable users to be created
        """Create, save and return a new user."""
        if not email:
            raise ValueError("No email provided.")

        email = self.normalize_email(email)  # normalize email
        user = self.model(email=email, **extra_fields)  # self.model refers to model associated with the manager
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create, save and return a new superuser."""
        extra_fields.setdefault("is_staff", True)  # assign default fields if not in extra_fields
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self.create_user(email, password, **extra_fields)
