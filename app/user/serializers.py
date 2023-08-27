"""
Serializers for user API view.
"""
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()  # Select model
        fields = ['email', 'password', 'name', 'date_joined']  # fields provided in a request
        extra_kwargs = {'password':{'write_only': True, 'min_length': 5}}  # extra meta data to prevent the password from being retrieved
        read_only_fields = ['date_joined']

    def create(self, validated_data):
        """Create and return user."""
        return get_user_model().objects.create_user(**validated_data)  # only called after data validation

    def update(self, instance, validated_data):
        """Update and return a user."""
        password = validated_data.pop("password", None)  # retrieve and remove password from validate data
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user token authentication."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, atrs):
        """Validate and authenticate the user."""
        email = atrs.get("email")
        password = atrs.get("password")

        user = authenticate(request=self.context.get('request'),  # attempt to authenticate the user
                            email=email,
                            password=password,)

        if not user:
            raise serializers.ValidationError("Unable to authenticate the user.", code='authorization')  # status.HTTP_401_UNAUTHORIZED

        atrs["user"] = user
        return atrs
