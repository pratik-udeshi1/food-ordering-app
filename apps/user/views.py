from django.contrib.auth import logout
from rest_framework import generics, views, parsers, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.models import User
from apps.user.serializers import UserRegistrationSerializer, UserLoginSerializer


class UserCreate(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    parser_classes = (parsers.JSONParser,)
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        response_data = {
            'message': 'User registered successfully',
            'user_id': user.id,
            'email': user.email,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLogin(TokenObtainPairView):
    serializer_class = UserLoginSerializer


class UserLogout(views.APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
