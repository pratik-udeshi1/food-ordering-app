from django.utils import timezone
from rest_framework import generics, status, filters
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from common import permissions, pagination
from common.constants import ApplicationMessages
from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantList(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsStaff]
    model = Restaurant
    queryset = Restaurant.objects.filter(deleted_at__isnull=True).order_by('id')
    filter_backends = [filters.SearchFilter]
    pagination_class = pagination.DefaultPagination
    search_fields = ['name', 'address']

    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            queryset = self.queryset.filter(pk=pk)
            if queryset.exists():
                result = queryset.first()
                serializer = self.serializer_class(result)
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise NotFound(detail=ApplicationMessages.NOT_FOUND)

        filtered_queryset = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(filtered_queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=pk)
        except Restaurant.DoesNotExist:
            raise NotFound(detail=ApplicationMessages.NOT_FOUND)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(pk=pk, deleted_at__isnull=True)
            instance.deleted_at = timezone.now()
            instance.save()
            return Response(ApplicationMessages.RECORD_DELETED, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response(ApplicationMessages.RECORD_NOT_DELETED, status=status.HTTP_400_BAD_REQUEST)
