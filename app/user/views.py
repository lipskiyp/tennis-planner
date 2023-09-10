"""
Views for the user API.
"""
from django.contrib.auth import get_user_model
from django.db.models import Q

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes

from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .permissions import IsStaffPermission
from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):  # handles http post requests
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Obtain user authentication token."""
    serializer_class = AuthTokenSerializer  # custom serializer with user email as the primary user identifier
    renderrer_classes = api_settings.DEFAULT_RENDERER_CLASSES # add browsable API

    def post(self, request, *args, **kwargs):
        """
        Customise authentication token view.
        https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
        """
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'email': user.email
        })


class ManageUserView(generics.RetrieveUpdateAPIView):  # handles http get, put and patch requests
    """Retrieve and update the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]  # authentication scheme
    permission_classes = [permissions.IsAuthenticated]  # ensure user is authenticated

    def get_object(self):  # retrieve the requesting user only
        """Retrieve and return the authenticated user."""
        return self.request.user



@extend_schema(
    parameters=[
        OpenApiParameter(
            'is_client',
            OpenApiTypes.BOOL,
            description="Users are client",
        ),
        OpenApiParameter(
            'is_coach',
            OpenApiTypes.BOOL,
            description="Users are coaches.",
        ),
        OpenApiParameter(
            'is_staff',
            OpenApiTypes.BOOL,
            description="Users are staff.",
        )
    ]
)
class UserView(generics.ListAPIView):  # list all user
    """Retrieve users."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]  # authentication scheme
    permission_classes = [permissions.IsAuthenticated, IsStaffPermission]  # ensure user is authenticated and staff

    def get_queryset(self):
        """Custom queryset logic for users."""
        queryset = get_user_model().objects.all()

        is_client = self.request.query_params.get('is_client')
        if is_client:
            queryset = queryset.filter(Q(is_coach=False) & Q(is_staff=False))

        is_coach = self.request.query_params.get('is_coach')
        if is_coach:
            queryset = queryset.filter(is_coach=bool(is_coach))

        is_staff = self.request.query_params.get('is_staff')
        if is_staff:
            queryset = queryset.filter(is_staff=bool(is_staff))

        return queryset
