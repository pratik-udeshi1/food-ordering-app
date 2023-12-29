# utils.py
import stripe

from apps.payment.models import PaymentMethod
from restaurant import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeHelper:
    @staticmethod
    def create_customer(name, email):
        try:
            customer = stripe.Customer.create(name=name, email=email)
            return customer.id
        except stripe.error.StripeError as e:
            raise Exception(f"create_customer--->{e}")

    @staticmethod
    def create_payment_method_in_stripe():
        try:
            # Frontend will provide this dynamic token which would be
            # generated after taking & processing user credit card details.
            token = 'tok_visa'

            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={'token': token},
            )

            return payment_method.id
        except stripe.error.StripeError as e:
            raise Exception(f"create_payment_method_in_stripe--->{e}")

    @staticmethod
    def add_card_to_customer(customer_id, pm_id):
        try:
            stripe.PaymentMethod.attach(pm_id, customer=customer_id)
            updated_customer = stripe.Customer.modify(customer_id, invoice_settings={
                'default_payment_method': pm_id,
            })
            return updated_customer
        except stripe.error.StripeError as e:
            raise Exception(f"add_card_to_customer--->{e}")

    @staticmethod
    def make_payment(user, amount, description):
        try:
            user_payment_info = PaymentMethod.objects.filter(user=user).first()
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                customer=user_payment_info.stripe_customer_id,
                payment_method=user_payment_info.stripe_payment_method_id,
                description=description,
            )
            return payment_intent.id
        except stripe.error.StripeError as e:
            raise Exception(f"make_payment--->{e}")
