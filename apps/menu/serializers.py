from rest_framework import serializers

from common.constants import ApplicationMessages
from .models import Menu
from ..restaurant.models import Restaurant


class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.UUIDField(write_only=True)

    class Meta:
        model = Menu
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        restaurant = validated_data.pop('restaurant', None)

        if restaurant:
            try:
                temp_restaurant = Restaurant.objects.get(pk=restaurant)
                validated_data['restaurant'] = temp_restaurant
            except Restaurant.DoesNotExist:
                raise serializers.ValidationError(ApplicationMessages.DOES_NOT_EXISTS.format('Restaurant'))

        menu_instance = super(MenuSerializer, self).create(validated_data)

        response_data = self.to_representation(menu_instance)
        response_data['restaurant'] = {
            'id': menu_instance.restaurant.id,
            'name': menu_instance.restaurant.name,
            'address': menu_instance.restaurant.address,
        }

        return response_data
