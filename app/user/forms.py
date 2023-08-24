"""
Custom user forms.
"""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form."""

    class Meta:
        model = CustomUser
        fields = ("email", 'password', 'name')


class CustomUserChangeForm(UserChangeForm):
    """Custom user change form."""

    class Meta:
        model = CustomUser
        fields = ("email", 'password', 'name')
