from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.models import Order
from customers.models import Customer
from products.models import Product

from .serializers import  OrderSerializer, OrderDetailSerializer
from rest_framework.permissions import BasePermission

class IsOwnerAndAuth(BasePermission):
	def has_object_permission(self, request, view, obj):
		try:
			return obj.user.user == request.user
		except:
			return False


	def has_permission(self, request, view):
		if request.user and request.user.is_authenticated:
			return True
		return False

class OrderAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsOwnerAndAuth]
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
   # def get_queryset(self, *args, **kwargs):
    #    return Order.objects.filter(user=self.request.user)


class OrderDetail(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    model = Order
    serializer_class= OrderSerializer

    def post(self,request,*args,**kwargs):
        data=request.data
        billing_profile = data.get('billing_profile')
        products = data.get('products')
        order_id = data.get('order_id')
        shipping_total = data.get('shipping_total')
        total = data.get('total')
        active = data.get('active')
        customer=Customer.objects.get(pk=billing_profile)
        order = Order.objects.create(billing_profile=customer, order_id=order_id,
                                     shipping_total=shipping_total, total=total)
       # order=products.add(products)
       # order=Order.objects.bulk_create([
        #    Order(billing_profile=Customer.objects.get(pk=billing_profile)),
         #   Order( order_id=" order_id"),
          #  Order(shipping_total=" shipping_total"),
          #  Order(total=" total"), ])
      #  products = [{
       #      "products[x]": products.add()
        #   }
         #   for x in order.products.all()]
        products=order.products.all()

        order.save(products)
        return Response("Order is placed")

