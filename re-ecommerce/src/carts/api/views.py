from django.views.generic.base import View
import datetime
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from rest_framework import generics, mixins, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404
from django.views.generic.detail import SingleObjectMixin, DetailView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from  .serializers import CartSerializer,CartCheckoutSerializer
from  carts.models import Cart
from products.models import Product
from products.api.views import ProductDetailAPIView

class CartHomeAPIView(APIView):
    serilizer_class= CartSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        products = [{

            "id": x.id,
            # "url": x.get_absolute_url(),
            "name": x.name,
            "price": x.price
        }
            for x in cart_obj.products.all()]
        if cart_obj.user is not None:
            user_obj=cart_obj.user.email
        else:
            user_obj =None

        cart_data = {"user": user_obj,"id": cart_obj.id,"products": products, "subtotal": cart_obj.subtotal,'updated': cart_obj.updated,
                     "total": cart_obj.total}

        return cart_data







class CartAPIUpdateView(APIView ):
    permission_classes         = [permissions.IsAuthenticated]
    serializer_class =CartSerializer



    def put(self, request):
            cart_obj = Cart.objects.new_or_get(request)
            product_id = request.POST.get('product_id')
            product_id = Product.objects.get(id=product_id)
            qs = Product.objects.filter(id=product_id)
            if qs.count() == 1:
                product_obj = qs.first()
                if product_obj not in cart_obj.products.all():
                    cart_obj.products.add(product_obj)
                request.session['cart_items'] = cart_obj.products.count()
            return Response(status=200, data={'message': 'Product has been added to cart'})

    def delete(self, request):
            product_id = request.POST.get('product_id')
            cart_obj = Cart.objects.new_or_get(request)
            product_id = Product.objects.get(id=product_id)
            qs = Product.objects.filter(id=product_id)
            if qs.count() == 1:
                product_obj = qs.first()
                if product_obj not in cart_obj.products.all():
                    cart_obj.products.remove(product_obj)
                request.session['cart_items'] = cart_obj.products.count()
            return Response(status=200, data={'message': 'Product has been added to cart'})
