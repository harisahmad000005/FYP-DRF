from django.conf.urls import url
from django.urls import path, re_path

from orders.api.views import OrderAPIView,OrderDetail
urlpatterns = [
    path('order', OrderAPIView.as_view() ,name= 'order'),
    path('order/detail', OrderDetail.as_view(), name='order-detail'),

]
