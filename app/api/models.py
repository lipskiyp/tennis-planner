"""
API models.
"""
from django.db import models

from user.models import CustomUser


class Court(models.Model):
    """Session model."""
    court_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return self.court_name


class TrainingSession(models.Model):
    """Session model."""
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client')
    coach = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, default=None, related_name='coach')
    session_date = models.DateField()
    session_time = models.TimeField()

    def __str__(self):
        return f"{self.id}. {self.client.name} on court: {self.court.court_name} at: {self.session_time} on: {self.session_date}"
