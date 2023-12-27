# serializers.py
from rest_framework import serializers

from .models import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            # Include only the necessary fields
            'user', 'stripe_customer_id', 'stripe_payment_method_id', 'card_type',
            'last_four_digits', 'expiration_month', 'expiration_year', 'is_default',
            'billing_address_line1', 'billing_address_line2',
            'billing_city', 'billing_state', 'billing_zip',
        ]
