from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.menu.models import Menu
from apps.order.models import Order, OrderItem
from apps.restaurant.models import Restaurant
from apps.user.tests.test_views import UserFactory


class OrderTests(APITestCase):
    def setUp(self):
        self.staff_user = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.staff_user.tokens()["access"])}')

        # Create sample data for testing
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", address="123 Test Street")
        self.menu_item = Menu.objects.create(name="Test Menu Item", price=10.00, category='veg')
        self.order_data = {
            "status": "pending",
            "restaurant": str(self.restaurant.id),
            "items": [
                {"menu_id": str(self.menu_item.id), "quantity": 2}
            ],
            "total": 20.00,
            "special_instructions": "No spicy"
        }

    def test_create_order(self):
        url = reverse('order-list', args=[str(self.restaurant.id)])
        response = self.client.post(url, self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_order(self):
        order = Order.objects.create(restaurant=self.restaurant, total=20.00, status="pending")
        OrderItem.objects.create(order=order, menu_item=self.menu_item, quantity=2, total=20.00)

        url = reverse('order-detail', args=[str(order.id), str(self.restaurant.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "pending")

    def test_list_orders(self):
        Order.objects.create(restaurant=self.restaurant, total=20.00, status="pending")
        url = reverse('order-list', args=[str(self.restaurant.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_partial_update_order(self):
        order = Order.objects.create(restaurant=self.restaurant, total=20.00, status="pending")
        url = reverse('order-detail', args=[str(order.id), str(self.restaurant.id)])
        updated_data = {
            "status": "completed",
            "special_instructions": "Extra spicy"
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, "completed")
        self.assertEqual(order.special_instructions, "Extra spicy")

    def test_delete_order(self):
        order = Order.objects.create(restaurant=self.restaurant, total=20.00, status="pending")
        url = reverse('order-detail', args=[str(order.id), str(self.restaurant.id)])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertIsNotNone(order.deleted_at)

    def test_search_orders(self):
        Order.objects.create(restaurant=self.restaurant, total=20.00, status="pending")
        url = reverse('order-list', args=[str(self.restaurant.id)]) + '?search=pending'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
