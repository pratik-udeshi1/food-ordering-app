from django.urls import path

from .views import MenuList

urlpatterns = [
    path('restaurant/<uuid:restaurant_id>', MenuList.as_view(), name='menu-list'),
    path('<uuid:menu_id>/restaurant/<uuid:restaurant_id>', MenuList.as_view(), name='menu-detail'),
]
