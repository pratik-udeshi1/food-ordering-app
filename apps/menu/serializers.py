from rest_framework import serializers

from common.constants import ApplicationMessages
from common.model_utils import get_object_or_notfound
from .models import Menu
from ..restaurant.models import Restaurant


class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.UUIDField(write_only=True)
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Menu
        fields = '__all__'

    def create(self, validated_data):
        restaurant = validated_data.pop('restaurant', None)

        if restaurant:
            restaurant_instance = get_object_or_notfound(Restaurant, id=restaurant)
            if not restaurant_instance:
                raise serializers.ValidationError(ApplicationMessages.DOES_NOT_EXISTS.format('Restaurant'))
        validated_data['restaurant'] = restaurant_instance

        # Extract the image from the validated data
        image_data = validated_data.pop('image', None)

        # Create the Menu instance
        menu_instance = Menu.objects.create(**validated_data)

        # Save the image if it exists
        if image_data:
            menu_instance.image.save("menu_image.jpg", image_data, save=True)

        # Format the response data including the restaurant details
        response_data = self.to_representation(menu_instance)

        response_data['restaurant'] = {
            'id': menu_instance.restaurant.id,
            'name': menu_instance.restaurant.name,
            'address': menu_instance.restaurant.address,
        }

        return response_data
