# views.py
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PaymentSerializer
from .utils import StripeHelper

# Set your Stripe API key
stripe.api_key = 'your_stripe_secret_key'


@permission_classes([IsAuthenticated])
class CreateCustomerView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')

        try:
            customer_id = StripeHelper.create_customer(email)
            return Response({'customer_id': customer_id, 'success': True})
        except stripe.error.StripeError as e:
            return Response({'error': str(e), 'success': False}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class AddCardToCustomerView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = serializer.validated_data.get('customer_id')
        card_token = serializer.validated_data.get('card_token')

        try:
            card_id = StripeHelper.add_card_to_customer(customer_id, card_token)
            return Response({'card_id': card_id, 'success': True})
        except stripe.error.StripeError as e:
            return Response({'error': str(e), 'success': False}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class AttachCardToCustomerView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = serializer.validated_data.get('customer_id')
        card_id = serializer.validated_data.get('card_id')

        try:
            StripeHelper.attach_card_to_customer(customer_id, card_id)
            return Response({'success': True})
        except stripe.error.StripeError as e:
            return Response({'error': str(e), 'success': False}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class MakePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = serializer.validated_data.get('customer_id')
        amount = serializer.validated_data.get('amount')
        description = serializer.validated_data.get('description')

        try:
            payment_intent_id = StripeHelper.make_payment(customer_id, amount, description)
            return Response({'payment_intent_id': payment_intent_id, 'success': True})
        except stripe.error.StripeError as e:
            return Response({'error': str(e), 'success': False}, status=status.HTTP_400_BAD_REQUEST)
