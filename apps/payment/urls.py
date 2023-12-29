from django.urls import path

from .views import CreateCustomerPaymentMethodView

urlpatterns = [
    path('create-customer/', CreateCustomerPaymentMethodView.as_view(), name='create_customer'),
]
