from django.utils import timezone
from rest_framework import generics, status, filters
from rest_framework.response import Response

from common import permissions, pagination
from common.constants import ApplicationMessages
from common.model_utils import filter_instance, get_object_or_notfound
from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantList(generics.ListCreateAPIView):
    model = Restaurant
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsStaff]
    pagination_class = pagination.DefaultPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']

    def get_queryset(self):
        return filter_instance(self.model, ordering='-created_at')

    def get(self, request, restaurant_id=None, *args, **kwargs):
        if restaurant_id:
            queryset = get_object_or_notfound(self.model, id=restaurant_id)
            serializer = self.serializer_class(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, restaurant_id, *args, **kwargs):
        restaurant = get_object_or_notfound(self.model, id=restaurant_id)
        serializer = self.serializer_class(restaurant, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, restaurant_id, *args, **kwargs):
        restaurant = get_object_or_notfound(self.model, id=restaurant_id)
        restaurant.deleted_at = timezone.now()
        restaurant.save()
        return Response(ApplicationMessages.RECORD_DELETED, status=status.HTTP_200_OK)
