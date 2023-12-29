from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.menu.models import Menu
from apps.restaurant.models import Restaurant
from apps.user.tests.test_views import UserFactory


class MenuTests(APITestCase):
    def setUp(self):
        self.staff_user = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.staff_user.tokens()["access"])}')

        # Create sample data for testing
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", address="123 Test Street")
        self.menu_data = {
            "name": "Test Menu Item",
            "description": "Delicious menu item",
            "price": 15.00,
            "category": "main",
            "classification": "vegan",
            "restaurant": str(self.restaurant.id),
            "spicy": True,
            "contains_peanuts": False,
            "gluten_free": True,
            "availability": True,
            "calories": "300",
        }

    def test_create_menu_item(self):
        url = reverse('menu-list', args=[str(self.restaurant.id)])
        response = self.client.post(url, self.menu_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_menu_item(self):
        menu_item = Menu.objects.create(**self.menu_data)
        url = reverse('menu-detail', args=[str(menu_item.id), str(self.restaurant.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Menu Item")
        # Add more assertions based on your data model

    def test_partial_update_menu_item(self):
        menu_item = Menu.objects.create(**self.menu_data)
        url = reverse('menu-detail', args=[str(menu_item.id), str(self.restaurant.id)])
        updated_data = {
            "price": 18.00,
            "spicy": False,
            "availability": False,
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        menu_item.refresh_from_db()
        self.assertEqual(menu_item.price, 18.00)
        self.assertFalse(menu_item.spicy)
        self.assertFalse(menu_item.availability)

    def test_delete_menu_item(self):
        menu_item = Menu.objects.create(**self.menu_data)
        url = reverse('menu-detail', args=[str(menu_item.id), str(self.restaurant.id)])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        menu_item.refresh_from_db()
        self.assertIsNotNone(menu_item.deleted_at)

    def test_search_menu_items(self):
        Menu.objects.create(**self.menu_data)
        url = reverse('menu-list', args=[str(self.restaurant.id)]) + '?search=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
