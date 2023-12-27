# utils.py
import stripe


class StripeHelper:
    @staticmethod
    def create_customer(email):
        try:
            customer = stripe.Customer.create(email=email)
            return customer.id
        except stripe.error.StripeError as e:
            raise e

    @staticmethod
    def add_card_to_customer(customer_id, card_token):
        try:
            card = stripe.Customer.create_source(customer=customer_id, source=card_token)
            return card.id
        except stripe.error.StripeError as e:
            raise e

    @staticmethod
    def attach_card_to_customer(customer_id, card_id):
        try:
            stripe.Customer.modify(customer_id, default_source=card_id)
            return True
        except stripe.error.StripeError as e:
            raise e

    @staticmethod
    def make_payment(customer_id, amount, description):
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                customer=customer_id,
                description=description,
            )
            return payment_intent.id
        except stripe.error.StripeError as e:
            raise e
