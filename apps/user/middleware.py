from django.http import HttpResponse
from rest_framework import status


class StripeProfileCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.user.payment_method_user:
                message = "Stripe profile doesn't exist. Please create signup for stripe profile, to access further"
                return HttpResponse(message, status=status.HTTP_400_BAD_REQUEST)

        response = self.get_response(request)
        return response
