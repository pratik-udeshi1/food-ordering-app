from django.urls import path

from apps.menu.views import MenuList
from .views import RestaurantList

urlpatterns = [
    path('', RestaurantList.as_view(), name='restaurant-list'),
    path('<uuid:restaurant_id>', RestaurantList.as_view(), name='restaurant-detail'),
]
