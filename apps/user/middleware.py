import uuid

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from common.constants import ApplicationMessages


class StripeProfileCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        api_views = '/api/v1'

        # Check if the request is within the specified 'api/v1' url route..
        if api_views in request.path_info and request.user.is_authenticated:
            has_payment_method = request.user.payment_method_user.exists()
            if not has_payment_method:
                response = Response(
                    data={
                        "success": False,
                        "code": 403,
                        "error": {
                            "traceId": uuid.uuid4(),
                            "message": [
                                ApplicationMessages.STRIPE_PROFILE_NOT_EXIST
                            ]
                        }
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response
        response = self.get_response(request)
        return response
