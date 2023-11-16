from django.db.models import Sum
from rest_framework import serializers

from .models import Order, OrderItem
from ..menu.models import Menu


class OrderSerializer(serializers.ModelSerializer):
    final_total = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        menu_items = validated_data.pop('menu_items', [])  # Retrieve menu items from validated_data

        # Calculate final_total using the Sum aggregation
        final_total = Menu.objects.filter(id__in=menu_items).aggregate(Sum('price'))['price__sum']

        # Set the calculated final_total in the validated_data
        validated_data['final_total'] = final_total

        order_instance = super(OrderSerializer, self).create(validated_data)

        # Create OrderItem instances for each menu item in the order
        for menu_id in menu_items:
            OrderItem.objects.create(order=order_instance, menu_item_id=menu_id)

        return order_instance
