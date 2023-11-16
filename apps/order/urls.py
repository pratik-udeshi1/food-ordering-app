from django.urls import path

from apps.order.views import OrderList

urlpatterns = [
    path('restaurant/<uuid:restaurant_id>', OrderList.as_view(), name='menu-list'),
    path('<uuid:order_id>/restaurant/<uuid:restaurant_id>', OrderList.as_view(), name='menu-detail'),
]
