from django.urls import path
from apps.user.views import UserCreate, UserLogin, UserLogout

urlpatterns = [
    path('register', UserCreate.as_view(), name='user-create'),
    path('login', UserLogin.as_view(), name='user-login'),
    path('logout', UserLogout.as_view(), name='user-logout'),
]
