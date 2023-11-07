from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.user.urls')),
    path('api/v1/restaurant/', include('apps.restaurant.urls')),
]
