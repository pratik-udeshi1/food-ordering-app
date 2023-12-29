from rest_framework import serializers

from common.constants import ApplicationMessages
from .models import PaymentMethod
from .utils import StripeHelper


class CreateCustomerSerializer(serializers.ModelSerializer):
    stripe_customer_id = serializers.CharField(write_only=True, required=False)
    stripe_payment_method_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = PaymentMethod
        exclude = ['user', ]

    def validate(self, data):
        user = self.context['request'].user
        existing_payment_method = PaymentMethod.objects.filter(user=user, deleted_at__isnull=True).first()

        if existing_payment_method:
            raise serializers.ValidationError(ApplicationMessages.STRIPE_CUST_EXIST)

        return data

    def create(self, validated_data):
        user = self.context['request'].user

        try:
            customer = StripeHelper.create_customer(user.full_name, user.email)
            payment_method = StripeHelper.create_payment_method_in_stripe()
            StripeHelper.add_card_to_customer(customer, payment_method)
        except Exception as e:
            # Log the error, and raise a validation error
            print(f"Stripe error: {str(e)}")
            raise serializers.ValidationError('Failed to create customer and payment method on Stripe.')

        validated_data['user'] = user
        validated_data['stripe_customer_id'] = customer
        validated_data['stripe_payment_method_id'] = payment_method

        # Create the PaymentMethod instance in the database
        card_instance = PaymentMethod(**validated_data, is_default=True)
        card_instance.save()
        return card_instance

    def to_representation(self, instance):
        # Return a serialized representation of the entire model
        representation = super().to_representation(instance)
        representation['stripe_customer_id'] = instance.stripe_customer_id
        representation['stripe_payment_method_id'] = instance.stripe_payment_method_id
        return representation
