import os
import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.menu.models import Menu
from apps.restaurant.models import Restaurant
from apps.user.tests.test_views import UserFactory

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nhp.settings")


class RestaurantListTests(APITestCase):
    def setUp(self):
        # Create a staff user or use an existing staff user for authentication
        # Make sure to adjust this based on your authentication logic
        self.staff_user = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.staff_user.tokens()["access"])}')

        # Create sample data for testing
        self.restaurant_data = {
            "name": "Test Restaurant",
            "address": "123 Test Street",
        }

        self.restaurant = Restaurant.objects.create(**self.restaurant_data)
        self.menu_data = {
            "name": "Test Menu",
            "restaurant": self.restaurant,
            "description": 'test',
            "price": 10.00,
            "category": 'veg',
        }
        Menu.objects.create(**self.menu_data)

    def tearDown(self):
        # Clear test data after each test
        Restaurant.objects.all().delete()
        Menu.objects.all().delete()

    def test_list_restaurants(self):
        url = reverse('restaurant-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_restaurant(self):
        self.restaurant_data["name"] = "Test_Restaurant" + str(uuid.uuid4())  # Unique name each time

        url = reverse('restaurant-list')
        response = self.client.post(url, self.restaurant_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_restaurant(self):
        url = reverse('restaurant-detail', args=[str(self.restaurant.id)])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.restaurant_data['name'])
        self.assertEqual(response.data['address'], self.restaurant_data['address'])

    def test_partial_update_restaurant(self):
        updated_data = {
            "name": "Updated Restaurant Name",
        }
        url = reverse('restaurant-detail', args=[str(self.restaurant.id)])
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, updated_data['name'])

    def test_delete_restaurant(self):
        url = reverse('restaurant-detail', args=[str(self.restaurant.id)])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.restaurant.refresh_from_db()
        self.assertIsNotNone(self.restaurant.deleted_at)

    def test_search_restaurants(self):
        # Assuming there is at least one restaurant in the database
        url = reverse('restaurant-list') + '?search=Test'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
