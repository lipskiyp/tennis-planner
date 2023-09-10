"""
Serializers for API view.
"""
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from api.models import Court, TrainingSession
from user.models import CustomUser
from user.serializers import UserSerializer


class CourtSerializer(serializers.ModelSerializer):
    """Serializer for the court object."""

    class Meta:
        model = Court
        fields = ['id', 'court_name', 'is_active', 'open_time', 'close_time']
        read_only_fields = ['id']


class TrainingSessionSerializer(serializers.ModelSerializer):
    """Serializer for the training session object."""
    court = CourtSerializer(read_only=True)
    court_id = serializers.PrimaryKeyRelatedField(source='court',
                                                  queryset=Court.objects.all(),
                                                  write_only=True)
    client = UserSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(source='client',
                                                   queryset=CustomUser.objects.all(),
                                                   write_only=True)
    coach = UserSerializer(read_only=True)
    coach_id = serializers.PrimaryKeyRelatedField(source='coach',
                                                  queryset=CustomUser.objects.all(),
                                                  write_only=True,
                                                  required=False)

    class Meta:
        model = TrainingSession
        fields = ['id', 'court', 'court_id', 'client', 'client_id', 'coach', 'coach_id', 'session_date', 'session_time']
        read_only_fields = ['id']

    def validate(self, attrs):
        """Validate new training session inputs."""
        # Ensure court is available.
        if TrainingSession.objects.filter(court=attrs.get('court'),
                                          session_date=attrs.get('session_date'),
                                          session_time=attrs.get('session_time')).exists():
                raise serializers.ValidationError("Court already booked.")

        # Ensure coach is available.
        if TrainingSession.objects.filter(coach=attrs.get('coach'),
                                          session_date=attrs.get('session_date'),
                                          session_time=attrs.get('session_time')).exists():
            raise serializers.ValidationError("Coach is not available.")

        return attrs
