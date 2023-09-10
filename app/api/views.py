"""
Views for the API.
"""
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes

from django.db.models import Q

import datetime

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes

from .serializers import CourtSerializer, TrainingSessionSerializer
from user.permissions import IsStaffPermission, IsStaffOrSessionClientCoachPermission
from .models import Court, TrainingSession


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'start_date',
                OpenApiTypes.STR,
                description="Session start date range.",
            ),
            OpenApiParameter(
                'end_date',
                OpenApiTypes.STR,
                description="Session end date range.",
            ),
            OpenApiParameter(
                'court',
                OpenApiTypes.INT,
                description="Court id.",
            )
        ]
    )
)
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
        queryset = self.queryset

        if not self.request.user.is_superuser or not self.request.user.is_staff:  # allow access to all training sessions for the superuser and staff only.
            queryset = queryset.filter(Q(client=self.request.user) | Q(coach=self.request.user))#.order_by('session_date', 'session_time')  # filter sessions where request user is client or coach.

        start_date = self.request.query_params.get('start_date')  # filter out all session before start_date
        if start_date:
            queryset = queryset.filter(session_date__gte=start_date)

        end_date = self.request.query_params.get('end_date')  # filter out all session after end_date
        if end_date:
            queryset = queryset.filter(session_date__lte=end_date)

        court = self.request.query_params.get('court')  # filter all sessions on court
        if court:
            queryset = queryset.filter(court=court)

        return queryset


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
