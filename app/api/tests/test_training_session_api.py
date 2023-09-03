"""
Tests for API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from api.models import TrainingSession
from api.tests.test_court_api import create_court
from api.serializers import TrainingSessionSerializer


TRAINING_SESSIONS_URL = reverse("api:sessions-list")


def create_training_session(court, client, **params):
    """Create and return a default training sessions."""
    defaults = {
        "session_date": "2023-10-09",
        "session_time": "20:00:00",
    }
    defaults.update(params)

    return TrainingSession.objects.create(court=court, client=client, **defaults)


class PublicTrainingSessionsAPITests(TestCase):
    """Tests for the training sessions API for an unauthenticated user."""
    def setUp(self):
        """Create an API client."""
        self.client = APIClient()

    def test_retrieve_training_sessions(self):
        """Test rerieving training sessions for an unauthenticated user."""
        res = self.client.get(TRAINING_SESSIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserTrainingSessionsAPITests(TestCase):
    """Tests for the training sessions API for an authenticated normal user."""
    def setUp(self):
        """Create an API client and a default user."""
        self.client = APIClient()
        self.court = create_court()  # default court
        payload = {
            'email': "user@example.com",
            'password': 'password123',
            'name': 'User',
        }
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**payload)
        self.client.force_authenticate(user=self.user)  # authenticate user

    def test_retrieving_training_session(self):
        """Test retrieving training session for an authenticated user."""
        training_session = create_training_session(court=self.court, client=self.user)

        url = reverse("api:sessions-detail", args=[training_session.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        training_session_obj = TrainingSession.objects.get(id=training_session.id)
        serializer = TrainingSessionSerializer(training_session_obj, many=False)
        self.assertEqual(res.data, serializer.data)

    def test_listing_training_sessions(self):
        """Test listing training sessions for an authenticated user."""
        another_user_payload = {
            "email": "anotheruser@example.com",
            "password": "pass123",
            "name": "Another User",
        }
        training_session = create_training_session(court=self.court, client=self.user)
        another_user = get_user_model().objects.create_user(**another_user_payload)
        create_training_session(court=self.court, client=another_user)  # session with another user

        res = self.client.get(TRAINING_SESSIONS_URL)  # list
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        training_session_obj = TrainingSession.objects.get(id=training_session.id)
        serializer = TrainingSessionSerializer(training_session_obj, many=False)
        self.assertEqual(res.data[0], serializer.data)  # check list is correct

    def test_listing_training_sessions_date_range(self):
        """Test listing training sessions for an authenticated user within a date range."""
        training_session_01 = create_training_session(court=self.court,
                                                      client=self.user,
                                                      session_date="2023-09-01")
        training_session_03 = create_training_session(court=self.court,
                                                      client=self.user,
                                                      session_date="2023-09-03")
        training_session_05 = create_training_session(court=self.court,
                                                      client=self.user,
                                                      session_date="2023-09-05")

        res = self.client.get(TRAINING_SESSIONS_URL, data={"start_date": "2023-09-03",
                                                           "end_date":"2023-09-03"})  # list
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        training_session_03_obj = TrainingSession.objects.get(id=training_session_03.id)
        serializer = TrainingSessionSerializer(training_session_03_obj, many=False)
        self.assertEqual(res.data[0], serializer.data)


    def test_creating_training_session(self):
        """Test creating a training session for an authenticated normal user."""
        res = self.client.post(TRAINING_SESSIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)  # only staff

class PrivateStaffTrainingSessionsAPITests(TestCase):
    """Tests for the training sessions API for an authenticated staff user."""
    def setUp(self):
        """Create API client and an authenticated staff user."""
        self.client = APIClient()  # api client
        self.court = create_court()  # default court
        user_payload = {
            'email': "test@example.com",
            'password': 'password123',
            'name': 'test',
        }
        self.user = get_user_model().objects.create_user(**user_payload)
        coach_payload = {
            "email": "coach@example.com",
            "password": "pass123",
            "name": "Coach",
        }
        self.coach = get_user_model().objects.create_user(**coach_payload)  # default coach
        self.user.is_staff = True  # create staff user
        self.client.force_authenticate(user=self.user)  # authenticate user

    def test_create_update_delete_training_session(self):
        """Test creating, updating and deleting training sessions for an authenticated user."""
        payload = {
            "court_id": self.court.id,
            "client_id": self.user.id,
            "coach_id": self.coach.id,
            "session_date": "2023-10-09",
            "session_time": "20:00:00",
        }
        res_create = self.client.post(TRAINING_SESSIONS_URL, payload)  # create training session
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)

        url = reverse("api:sessions-detail", args=[res_create.data["id"]])

        new_session_date = "2023-09-09"
        res_update = self.client.patch(url, {"session_date": new_session_date})
        self.assertEqual(res_update.status_code, status.HTTP_200_OK)  # check sessions was updated
        self.assertEqual(res_update.data["session_date"], new_session_date)

        res_delete = self.client.delete(url)
        training_session_exists = TrainingSession.objects.filter(id=res_create.data["id"]).exists()
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(training_session_exists)
