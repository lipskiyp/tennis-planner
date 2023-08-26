"""
Custom Django admin.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.forms import CustomUserCreationForm, CustomUserChangeForm
from user.models import CustomUser
from api.models import Court, TrainingSession


class CustomUserAdmin(UserAdmin):
    """Custom user admin."""
    ordering = ('id',)
    search_fields = ("email",)

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("id", "email", "name", "date_joined", "is_coach", "is_staff", "is_active", "is_superuser",)
    list_filter = ("email", "is_coach", "is_staff", "is_active", "is_superuser", )

    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        ("Permissions", {"fields": ("is_coach", "is_staff", "is_active", 'is_superuser',)}),
        ('Important dates', {'fields':('last_login',)}),
    )
    readonly_fields = ['last_login'] #  prevent it from being modified

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'password1', 'password2',
                'is_coach', 'is_active', 'is_staff', 'is_superuser',
            )
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Court)
admin.site.register(TrainingSession)
