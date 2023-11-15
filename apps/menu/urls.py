from django.urls import path

from .views import MenuList

urlpatterns = [
    path('menu', MenuList.as_view(), name='menu-list'),
    path('menu/<uuid:menu_id>', MenuList.as_view(), name='menu-detail'),
]
