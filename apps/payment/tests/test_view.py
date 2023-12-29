import os

from apps.user.tests.test_views import UserFactory
from django.urls import reverse
from faker import factory
from rest_framework import status

from apps.payment.models import PaymentMethod

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant.settings")


class PaymentMethodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentMethod

    # Add any necessary attributes for PaymentMethod


class StripePaymentAPITest(APITestCase):
    """Testing Stripe payment module"""

    def setUp(self):
        """Set up test database"""
        self.user = UserFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.user.tokens()["access"])}')

    def test_create_customer(self):
        """Test creating a new customer in Stripe"""
        payload = {
            "email": "test@example.com",
            # Add other required fields for customer creation
        }

        url = reverse("create_customer")
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_card_to_customer(self):
        """Test adding a card to an existing customer in Stripe"""
        customer_id = "test_customer_id"  # Replace with a valid customer ID
        payload = {
            "customer_id": customer_id,
            "card_token": "test_card_token",  # Replace with a valid card token
        }

        url = reverse("add_card_to_customer")
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_attach_card_to_customer(self):
        """Test attaching a card to a customer in Stripe"""
        customer_id = "test_customer_id"  # Replace with a valid customer ID
        card_id = "test_card_id"  # Replace with a valid card ID
        payload = {
            "customer_id": customer_id,
            "card_id": card_id,
        }

        url = reverse("attach_card_to_customer")
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_make_payment(self):
        """Test making a payment using a customer in Stripe"""
        customer_id = "test_customer_id"  # Replace with a valid customer ID
        payload = {
            "customer_id": customer_id,
            "amount": 100,  # Replace with a valid amount
            "description": "Test Payment",
        }

        url = reverse("make_payment")
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
