"""
Custom permissions for the API.
"""
from rest_framework import permissions


class IsStaffPermission(permissions.BasePermission):
    """Global permission to only allow allows staff."""
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        return False


class IsCoachPermission(permissions.BasePermission):
    """Global permission to only allows coaches."""
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_coach:
            return True
        return False


class IsStaffOrSessionClientCoachPermission(permissions.BasePermission):
    """Object level permission to only allow staff or session client or session coach."""
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_staff or request.user in [obj.client, obj.coach]:
            return True
        return False
