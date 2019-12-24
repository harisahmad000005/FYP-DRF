from django.conf.urls import url
from django.urls import path, re_path

from carts.api.views import CartHomeAPIView, CartAPIUpdateView
urlpatterns = [
     path('cart', CartHomeAPIView.as_view(),name= 'cart'),
     path('cart/update/', CartAPIUpdateView.as_view(), name='cart-update'),

]
