from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.user.views import UserCreate, UserLogin, UserLogout

urlpatterns = [
    path('register', UserCreate.as_view(), name='user-create'),
    path('login', UserLogin.as_view(), name='user-login'),
    path('logout', UserLogout.as_view(), name='user-logout'),
]

urlpatterns += [
    path('gettoken/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('refreshtoken/', TokenRefreshView.as_view(), name="token_refresh"),
    path('verifytoken/', TokenVerifyView.as_view(), name="token_verify"),
]
