from rest_framework import generics, status, filters
from rest_framework.response import Response

from common import permissions, pagination
from common.model_utils import get_object_or_notfound, filter_instance
from .models import Order
from .serializers import OrderSerializer


class OrderList(generics.ListCreateAPIView):
    model = Order
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsStaff]
    pagination_class = pagination.DefaultPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        kwargs = {'restaurant': restaurant_id}
        _status = self.request.GET.get('status')
        if _status:
            kwargs['status'] = _status
        return filter_instance(self.model, ordering='-created_at', **kwargs)

    def get(self, request, order_id=None, *args, **kwargs):
        request.data['restaurant'] = self.kwargs.get('restaurant_id')
        request.data['status'] = request.GET.get('status')
        if order_id:
            queryset = get_object_or_notfound(self.model, id=order_id)
            serializer = self.serializer_class(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['restaurant'] = self.kwargs.get('restaurant_id')
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(order, status=status.HTTP_201_CREATED)
