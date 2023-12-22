import os

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nhp.settings")

# apps/user/tests/factories.py

import factory
from faker import Faker
from django.contrib.auth import get_user_model

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        skip_postgeneration_save = True

    email = factory.LazyAttribute(lambda _: fake.email())
    full_name = factory.LazyAttribute(lambda _: fake.name())
    password = factory.PostGenerationMethodCall('set_password', 'testpassword')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to set the password properly."""
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class UserAPITest(APITestCase):
    """Testing user registration and login"""

    def setUp(self):
        """Set up test database"""
        self.user = UserFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.user.tokens()["access"])}')

    def test_user_registration(self):
        """Test user registration"""
        payload = {
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
            # Add other required fields
        }

        url = reverse("user-create")
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_with_wrong_format(self):
        """Test that user won't be registered if fields are missing or mismatch"""
        payload = {
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
            "invalid_field": "value",  # Add an invalid field
        }

        url = reverse("user-create")
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_user_login(self):
    #     """Test user login"""
    #     payload = {
    #         "email": self.user.email,
    #         "password": "testpassword",
    #     }
    #
    #     url = reverse("token_obtain_pair")
    #     response = self.client.post(url, payload, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn("access", response.data)
    #     self.assertIn("refresh", response.data)
    #
    # def test_user_login_with_wrong_credentials(self):
    #     """Test user login with wrong credentials"""
    #     payload = {
    #         "email": self.user.email,
    #         "password": "wrongpassword",
    #     }
    #
    #     url = reverse("token_obtain_pair")
    #     response = self.client.post(url, payload, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
