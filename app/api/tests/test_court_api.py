"""
Tests for API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from api.models import Court
from api.serializers import CourtSerializer


COURTS_URL = reverse("api:courts-list")


def create_court(**params):
    """Create and return a default cort."""
    defaults = {
        "court_name": "Example",
        "open_time": "09:00:00",
        "close_time": "20:00:00",
    }
    defaults.update(params)

    return Court.objects.create(**defaults)


class PublicCourtsAPITests(TestCase):
    """Tests for the courts API for an unauthenticated user."""
    def setUp(self):
        """Create an API client."""
        self.client = APIClient()

    def test_retrieve_courts(self):
        """Test retrieving courts for an unauthenticated user."""
        res = self.client.get(COURTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_court(self):
        """Test creating a court for an unauthenticated user."""
        res = self.client.post(COURTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserCourtsAPITests(TestCase):
    """Tests for the courts API for an authenticated normal user."""
    def setUp(self):
        """Create an API client and a default user."""
        self.client = APIClient()
        payload = {
            'email': "test@example.com",
            'password': 'password123',
            'name': 'test',
        }
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**payload)
        self.client.force_authenticate(user=self.user)  # authenticate user

    def test_retrieving_courts(self):
        """Test retrieving courts for an authenticated normal user."""
        payload = {
            "court_name": "Court",
            "open_time": "09:00:00",
            "close_time": "20:00:00",
        }
        court = create_court(**payload)

        url = reverse("api:courts-detail", args=[court.id])  # court url
        res = self.client.get(url)  # retrieve court via API
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        court_obj = Court.objects.get(id=court.id)
        serializer = CourtSerializer(court_obj, many=False)
        self.assertEqual(res.data, serializer.data)  # check court is retrieved correctly

    def test_listing_courts(self):
        """Test listing courts for an authenticated normal user."""
        create_court(court_name="Court 1")
        create_court(court_name="Court 2")  # create 2 courts

        res = self.client.get(COURTS_URL)  # list all courts
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        courts = Court.objects.all()
        serializer = CourtSerializer(courts, many=True)
        self.assertEqual(res.data, serializer.data)  # check courts are listed correctly

    def test_creating_court(self):
        """Test creating a court for an authenticated normal user."""
        res = self.client.post(COURTS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)  # only staff


class PrivateStaffCourtsAPITests(TestCase):
    """Tests for the courts API for an authenticated staff user."""
    def setUp(self):
        """Create an API client and an authenticated staff user."""
        self.client = APIClient()
        payload = {
            'email': "test@example.com",
            'password': 'password123',
            'name': 'test',
        }
        self.user = get_user_model().objects.create_user(**payload)
        self.user.is_staff = True  # create staff user
        self.client.force_authenticate(user=self.user)  # authenticate user

    def test_creating_updating_deleting_court(self):
        """Test creating, updating and deleting a court for an authenticated staff user."""
        payload = {
            "court_name": "Court",
            "open_time": "08:00:00",
            "close_time": "21:00:00",
        }
        res_create = self.client.post(COURTS_URL, payload)  # test creating a court
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)

        court = Court.objects.get(id=res_create.data["id"])
        serializer = CourtSerializer(court, many=False)
        self.assertEqual(res_create.data, serializer.data)  # check court is retrieved correctly

        url = reverse("api:courts-detail", args=[res_create.data["id"]]) # court url

        new_court_name = "New Name"
        res_update = self.client.patch(url, {"court_name": new_court_name})  # test updating a court
        self.assertEqual(res_update.status_code, status.HTTP_200_OK)
        self.assertEqual(res_update.data["court_name"], new_court_name)

        res_delete = self.client.delete(url)  # test deleting a court
        court_exists = Court.objects.filter(id=res_create.data["id"]).exists()
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(court_exists)
