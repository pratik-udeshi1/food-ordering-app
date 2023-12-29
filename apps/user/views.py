from django.contrib.auth import logout
from rest_framework import generics, views, parsers, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.api_response import ApiResponse
from apps.user.serializers import UserRegistrationSerializer, UserLoginSerializer


class UserCreate(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    parser_classes = (parsers.JSONParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = ApiResponse.create_api_response(serializer)

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLogin(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            response = super().post(request, *args, **kwargs)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(views.APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
