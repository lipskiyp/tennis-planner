"""
Views for the API.
"""
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import CourtSerializer, TrainingSessionSerializer
from .permissions import IsStaffPermission, IsCoachPermission, IsStaffOrSessionClientCoachPermission
from .models import Court, TrainingSession


class TrainingSessionViewSet(viewsets.ModelViewSet):
    """Viewset to manage training sessions."""
    serializer_class = TrainingSessionSerializer
    queryset = TrainingSession.objects.all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_permissions(self):
        """Instantiates and returns the list of permissions for the view."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsStaffOrSessionClientCoachPermission]
        else:
            permission_classes = [IsAuthenticated, IsStaffPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Custom queryset logic for the training sessions."""
        if self.request.user.is_superuser or self.request.user.is_staff:
            return self.queryset  # allow access to all training sessions for the superuser and staff only.
        else:
            return self.queryset.filter(Q(client=self.request.user) | Q(coach=self.request.user))  # filter sessions where request user is client or coach.


class CourtViewSet(viewsets.ModelViewSet):
    """Viewset to manage courts."""
    serializer_class = CourtSerializer
    queryset = Court.objects.all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions for the view.
        https://www.django-rest-framework.org/api-guide/viewsets/#introspecting-viewset-actions
        """
        if self.action in ['list', 'retrieve']:  # allow any authenticated user to list and retrieve court object
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsStaffPermission]
        return [permission() for permission in permission_classes]
