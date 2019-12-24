from django.conf.urls import url
from django.urls import path, re_path

from products.api.views import ProductListAPIView, ProductDetailAPIView

urlpatterns = [
    path('product/', ProductListAPIView.as_view() ,name= 'list'),
    path('product/<id>', ProductDetailAPIView.as_view(), name='product-detail'),

]
