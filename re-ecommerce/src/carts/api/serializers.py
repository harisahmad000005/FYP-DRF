from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as api_reverse
from customers.api.serializers import CustomerLogInSerializer
from carts.models import Cart

jwt_payload_handler              = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler               = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler     = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta                     = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class CartSerializer(serializers.ModelSerializer):

    class Meta:
         model=Cart
         fields=[
             'id',
             'user',
             'products',
             'updated',
             'subtotal',
             'total',
         ]

    def get_product(self, obj):
        return obj.product.title
    def get_user(self, obj):
        return obj.user.email


class CartCheckoutSerializer(serializers.Serializer):
    token   = serializers.SerializerMethodField(read_only=True)
    uri     = serializers.SerializerMethodField(read_only=True)
    class Meta:
         model=Cart
         fields=[
             'token',
             'total',
              'uri'
                  ]

    def get_token(self, obj):
        checkout = obj
        payload = jwt_payload_handler(checkout)
        token = jwt_encode_handler(payload)
        return token

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('api-customer:login', kwargs={'id': obj.id}, request=request)

