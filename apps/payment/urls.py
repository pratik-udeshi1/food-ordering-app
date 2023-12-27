# urls.py

from django.urls import path

from .views import CreateCustomerView, AddCardToCustomerView, AttachCardToCustomerView, MakePaymentView

urlpatterns = [
    path('create-customer/', CreateCustomerView.as_view(), name='create_customer'),
    path('add-card-to-customer/', AddCardToCustomerView.as_view(), name='add_card_to_customer'),
    path('attach-card-to-customer/', AttachCardToCustomerView.as_view(), name='attach_card_to_customer'),
    path('make-payment/', MakePaymentView.as_view(), name='make_payment'),
]
