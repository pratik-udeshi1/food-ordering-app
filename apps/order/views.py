import stripe
from rest_framework import generics, status, filters
from rest_framework.response import Response

from common import permissions, pagination
from common.model_utils import get_object_or_notfound, filter_instance
from .models import Order
from .serializers import OrderSerializer
from ..payment.models import PaymentMethod


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

    def post_old(self, request, order_id, *args, **kwargs):
        order = Order.objects.get(id=order_id)

        # Get payment details from the request
        card_type = request.data.get('card_type')
        last_four_digits = request.data.get('last_four_digits')
        expiration_month = request.data.get('expiration_month')
        expiration_year = request.data.get('expiration_year')

        billing_address_line1 = request.data.get('billing_address_line1')
        billing_address_line2 = request.data.get('billing_address_line2')
        billing_city = request.data.get('billing_city')
        billing_state = request.data.get('billing_state')
        billing_zip = request.data.get('billing_zip')

        # Create a payment method in Stripe
        try:
            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={
                    'number': '4242424242424242',  # Example card number, replace with user input
                    'exp_month': expiration_month,
                    'exp_year': expiration_year,
                    'cvc': '123',  # Example CVC, replace with user input
                },
            )

            # Create a customer in Stripe
            customer = stripe.Customer.create(email=request.user.email, payment_method=payment_method.id)

            # Save the payment method details in your database (assuming you have a user)
            payment_method_instance = PaymentMethod.objects.create(
                user=request.user,
                stripe_customer_id=customer.id,
                stripe_payment_method_id=payment_method.id,
                card_type=card_type,
                last_four_digits=last_four_digits,
                expiration_month=expiration_month,
                expiration_year=expiration_year,
                billing_address_line1=billing_address_line1,
                billing_address_line2=billing_address_line2,
                billing_city=billing_city,
                billing_state=billing_state,
                billing_zip=billing_zip,
            )

            # Link the payment method to the order
            order.payment_method = payment_method_instance
            order.save()

            # Charge the customer for the order total
            charge = stripe.Charge.create(
                amount=int(order.total * 100),  # Convert total amount to cents
                currency='usd',  # Change to your currency code
                customer=customer.id,
                description=f'Payment for Order {order.id}',
            )

            # Update your order's payment_status
            order.payment_status = 'paid'
            order.save()

            return Response('Payment successful!', status=status.HTTP_201_CREATED)

        except stripe.error.CardError as e:
            # Handle card errors (e.g., insufficient funds, expired card)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
