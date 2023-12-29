from rest_framework import generics, status, permissions
from rest_framework.response import Response

from common.constants import ApplicationMessages
from .serializers import CreateCustomerSerializer


class CreateCustomerPaymentMethodView(generics.CreateAPIView):
    serializer_class = CreateCustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {'message': ApplicationMessages.STRIPE_CUST_PM_SUCCESS, 'data': serializer.data}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
