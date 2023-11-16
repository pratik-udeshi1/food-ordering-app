from rest_framework import serializers

from common.constants import ApplicationMessages
from common.model_utils import get_object_or_notfound
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
            restaurant_instance = get_object_or_notfound(Restaurant, id=restaurant)
            if not restaurant_instance:
                raise serializers.ValidationError(ApplicationMessages.DOES_NOT_EXISTS.format('Restaurant'))
        validated_data['restaurant'] = restaurant_instance
        menu_instance = super(MenuSerializer, self).create(validated_data)

        response_data = self.to_representation(menu_instance)
        response_data['restaurant'] = {
            'id': menu_instance.restaurant.id,
            'name': menu_instance.restaurant.name,
            'address': menu_instance.restaurant.address,
        }

        return response_data
