from django.conf.urls import url
from django.urls import path, re_path

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from customers.api.views import (
  CustomerRegisterAPIView,
   CustomerAuthAPIView,
 )
urlpatterns = [
    path('customer/register', CustomerRegisterAPIView.as_view() ,name= 'register'),
    path('customer/login', CustomerAuthAPIView.as_view() ,name= 'login'),
    path('jwt/', obtain_jwt_token, ),
    path('jwt/refresh', refresh_jwt_token, ),
]
