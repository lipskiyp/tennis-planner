"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .permissions import IsStaffPermission
from .serializers import UserSerializer, AuthTokenSerializer
from .models import CustomUser


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
