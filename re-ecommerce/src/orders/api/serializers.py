from rest_framework import serializers
from orders.models import Order
from products.models import Product
from products.api.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'billing_profile',
            'order_id',
             'products',
            'shipping_total',
            'total',
            'active',
               ]


class OrderDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="order_detail_api")
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "url",
            "order_id",
            "user",
            "billing_address",
            "subtotal",
            "order_total",
        ]

    def get_subtotal(self, obj):
        return obj.cart.subtotal
