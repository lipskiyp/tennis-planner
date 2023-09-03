"""
Tests for user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("api:user:create")
TOKEN_URL = reverse("api:user:token")
ME_URL = reverse("api:user:me")


class PublicUserAPITests(TestCase):
    """User API tests for an unauthorized user."""
    def setUp(self):
        """Create an API client."""
        self.client = APIClient()

    def test_creating_user(self):
        """Test creating a new user."""
        payload = {
            "email": "user@example.com",
            "name": "User",
            "password": "pass123",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", res.data)

        user = get_user_model().objects.get(email=payload["email"])
        self.assertAlmostEqual(user.name, payload["name"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_creating_user_without_email(self):
        """Test creating a new user without an email."""
        payload = {
            "name": "User",
            "password": "pass123",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_user_email_taken(self):
        """Test creating a user with an email that is already taken."""
        payload = {
            "email": "user@example.com",
            "name": "User",
            "password": "pass123",
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_token_user(self):
        """Test retrieving user token."""
        payload = {
            "email": "user@example.com",
            "name": "User",
            "password": "pass123",
        }
        get_user_model().objects.create_user(**payload)

        res = self.client.post(TOKEN_URL, {
            "email": payload.get("email"),
            "password": payload.get("password"),
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_retrieve_token_invalid_credential(self):
        """Test retrieving token with invalid credentials."""
        payload = {
            "email": "user@example.com",
            "name": "User",
            "password": "pass123",
        }
        get_user_model().objects.create_user(**payload)

        res = self.client.post(TOKEN_URL, {
            "email": payload.get("email"),
            "password": "wrongpass",
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrieve_user_unauthorized(self):
        """Test retrieiving user when user is unauthorized."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """User API tests for an authorized user."""
    def setUp(self):
        """Create an API client and authenticate a default user."""
        payload = {
            'email': "test@example.com",
            'password': 'password123',
            'name': 'test',
        }
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**payload)
        self.client.force_authenticate(user=self.user)  # authenticate user

    def test_retrieve_user_authorized(self):
        """Test retrieving user when user is authorized."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], self.user.email)
        self.assertEqual(res.data["name"], self.user.name)
