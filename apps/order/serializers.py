from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem
from ..menu.models import Menu


class OrderSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    items = serializers.ListField(write_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        menu_items = validated_data.pop('items', [])
        validated_data['total'] = Decimal('0')

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

            OrderItem.objects.bulk_create(order_items)

            order_instance.save()

        response_data = self.to_representation(order_instance)
        response_data['menu_items'] = self.get_menu_items_data(order_items)

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
