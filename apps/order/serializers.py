from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from common.constants import ApplicationMessages
from .models import Order, OrderItem
from ..menu.models import Menu
from ..payment.utils import StripeHelper


class OrderSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    items = serializers.ListField(write_only=True)
    user = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        menu_items = validated_data.pop('items', [])
        validated_data['total'] = Decimal('0')
        user = self.context['request'].user
        validated_data['user'] = user

        with transaction.atomic():
            order_instance = super(OrderSerializer, self).create(validated_data)

            order_items = []
            for menu_item_data in menu_items:
                menu_item_id = menu_item_data["menu_id"]
                quantity = menu_item_data["quantity"]

                menu_item = Menu.objects.get(id=menu_item_id)
                total_item_price = Decimal(menu_item.price * quantity)

                order_items.append(OrderItem(
                    order=order_instance,
                    menu_item_id=menu_item_id,
                    quantity=quantity,
                    total=total_item_price
                ))

                order_instance.total += total_item_price

            try:
                cents_amount = int(order_instance.total * 100)
                payment = StripeHelper.make_payment(user, cents_amount, str(order_instance.id))
                order_instance.status = 'processing'
                order_instance.payment_status = 'success'
                order_instance.payment_intent = payment
                OrderItem.objects.bulk_create(order_items)
                order_instance.save()
            except Exception as e:
                print(f"Stripe payment error: {str(e)}")
                raise serializers.ValidationError(ApplicationMessages.STRIPE_PAYMENT_FAIL)

        response_data = self.to_representation(order_instance)
        response_data['menu_items'] = self.get_menu_items_data(order_items)
        response_data['payment_details'] = ApplicationMessages.STRIPE_PAYMENT_SUCCESS

        return response_data

    def get_menu_items_data(self, order_items):
        # Extract relevant information from the Menu objects in order_items
        menu_items_data = []
        for order_item in order_items:
            menu_item_data = {
                'menu_id': order_item.menu_item.id,
                'quantity': order_item.quantity,
                'total': order_item.total,
                'menu_name': order_item.menu_item.name,
                'menu_description': order_item.menu_item.description,
                'menu_price': order_item.menu_item.price,
                'menu_category': order_item.menu_item.category,
                'menu_classification': order_item.menu_item.classification,
                'spicy': order_item.menu_item.spicy,
                'contains_peanuts': order_item.menu_item.contains_peanuts,
                'gluten_free': order_item.menu_item.gluten_free,
                'availability': order_item.menu_item.availability,
                'calories': order_item.menu_item.calories,
            }
            menu_items_data.append(menu_item_data)

        return menu_items_data
