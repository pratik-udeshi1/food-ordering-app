from django.utils import timezone
from rest_framework import generics, status, filters
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from common import permissions, pagination
from common.constants import ApplicationMessages
from common.model_utils import filter_instance, get_object_or_notfound
from .models import Menu
from .serializers import MenuSerializer


class MenuList(generics.ListCreateAPIView):
    model = Menu
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsStaff]
    pagination_class = pagination.DefaultPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category', 'classification']

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        kwargs = {'restaurant_id': restaurant_id}
        return filter_instance(self.model, ordering='-created_at', **kwargs)

    def get(self, request, *args, **kwargs):
        restaurant_id = self.kwargs.get('restaurant_id')
        menu_id = self.kwargs.get('menu_id')
        if menu_id:
            queryset = get_object_or_notfound(self.model, restaurant__id=restaurant_id, id=menu_id)
            serializer = self.serializer_class(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['restaurant'] = self.kwargs.get('restaurant_id')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        menu_item = serializer.save()
        return Response(menu_item, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        restaurant_id = self.kwargs.get('restaurant_id')
        menu_id = self.kwargs.get('menu_id')
        menu = get_object_or_notfound(self.model, restaurant__id=restaurant_id, id=menu_id)
        if menu.restaurant.deleted_at is not None:
            raise NotFound(detail=ApplicationMessages.NOT_FOUND)
        serializer = self.serializer_class(menu, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        restaurant_id = self.kwargs.get('restaurant_id')
        menu_id = self.kwargs.get('menu_id')
        menu = get_object_or_notfound(self.model, restaurant__id=restaurant_id, id=menu_id)
        menu.deleted_at = timezone.now()
        menu.save()
        return Response(ApplicationMessages.RECORD_DELETED, status=status.HTTP_200_OK)
