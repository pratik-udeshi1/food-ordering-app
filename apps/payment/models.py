from django.db import models

from apps.user.models import User
from common.models import BaseModel


class PaymentMethod(BaseModel):
    CARD_TYPE_CHOICES = (
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('amex', 'American Express'),
        ('discover', 'Discover'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_method_user')
    stripe_customer_id = models.CharField(max_length=255)  # Stripe Customer ID associated with the user
    stripe_payment_method_id = models.CharField(max_length=255)  # Stripe Payment Method ID
    is_default = models.BooleanField(default=False, help_text="Is this the user's default payment method?")

    billing_address_line1 = models.CharField(max_length=255, null=True, blank=True)
    billing_address_line2 = models.CharField(max_length=255, null=True, blank=True)
    billing_city = models.CharField(max_length=255, null=True, blank=True)
    billing_state = models.CharField(max_length=255, null=True, blank=True)
    billing_zip = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        # Enforce that there is only one default payment method per user
        unique_together = ('user', 'is_default')

    def __str__(self):
        return f"{self.card_type} ending in {self.last_four_digits}"
