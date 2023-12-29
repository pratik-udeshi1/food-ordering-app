from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user.models import User, Role
from common.model_utils import get_or_create_instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'full_name', 'phone_number', 'role_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    @staticmethod
    def get_role_name(obj):
        if obj.role:
            return obj.role.name
        else:
            return "No Role Assigned"  # Handle the case when there's no role assigned to the user

    def create(self, validated_data):
        filter_kwargs = {'name': 'staff'}  # Assigning Default Role as "Staff" for every new registration.
        validated_data['role'] = get_or_create_instance(Role, create_kwargs={}, **filter_kwargs)
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        login(self.context['request'], user)

        data = super().validate(attrs)
        user = self.user

        if user and user.role and user.role.name == 'staff':
            return {
                'user_id': user.id,
                'email': user.email,
                'access_token': data['access'],
                'refresh_token': data['refresh']
            }
        else:
            raise serializers.ValidationError("Only users with the 'staff' role can log in.")
