from rest_framework import generics, status, filters
from rest_framework.response import Response

from common import permissions, pagination
from .models import Order
from .serializers import OrderSerializer


class OrderList(generics.ListCreateAPIView):
    model = Order
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsStaff]
    pagination_class = pagination.DefaultPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']

    # def get_queryset(self):
    #     return filter_instance(self.model, ordering='-created_at')
    #
    # def get(self, request, order_id=None, *args, **kwargs):
    #     if order_id:
    #         queryset = get_object_or_notfound(self.model, id=order_id)
    #         serializer = self.serializer_class(queryset)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['restaurant'] = self.kwargs.get('restaurant_id')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def patch(self, request, order_id, *args, **kwargs):
    #     order = get_object_or_notfound(self.model, id=order_id)
    #     serializer = self.serializer_class(order, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def delete(self, request, order_id, *args, **kwargs):
    #     order = get_object_or_notfound(self.model, id=order_id)
    #     order.deleted_at = timezone.now()
    #     order.save()
    #     return Response(ApplicationMessages.RECORD_DELETED, status=status.HTTP_200_OK)
