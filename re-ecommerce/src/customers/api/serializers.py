from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.models import Q
from rest_framework_jwt.settings import api_settings
import datetime
from rest_framework.response import Response

from django.utils import timezone
from rest_framework.reverse import reverse as api_reverse
from rest_framework.validators import UniqueValidator

from customers.models import Customer


jwt_payload_handler              = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler               = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler     = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta                     = api_settings.JWT_REFRESH_EXPIRATION_DELTA

class CustomerListSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model =User
        fields=[
          'id',
            'email',
            'uri'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('api-customer:list', kwargs={'id': obj.id}, request=request)


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password =serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = Customer
        fields = ['first_name','last_name','email','password','password2'
                  , 'phone_number','address_line_1','address_line_2','city'
                  ,'postal_code']
        extra_kwargs = {'password': {'write_only': True},'password2': {'write_only': True}}



    def validate_email(self, value):
        qs = Customer.objects.filter(email__iexact=value)
        if qs.exists():
            return Response('Email Already Exists or it is not a valid email address ')
        return value


  #  def validate_password(self, data):
   #      pw =self.get('password')
    #     pw2 =self.get('password2')
     #    if pw != pw2:
      #      raise serializers.ValidationError('Passwords Must Match')
       #  return data


  #  def validate_phone_number(self,value):
   #     pn=value.get('phone_number')
    #    if pn.lenght() ==11:
     #       return pn
      #  else:
       #     raise serializers.ValidationError('Enter a Valid Phone Number')


    def create(self, obj):
          email     = obj.get('email')
          password  = obj.get('password')
          password2 = obj.get('password2')
          first_name = obj.get('first_name')
          last_name = obj.get('last_name')
          phone_number = obj.get('phone_number')
          address_line_1 = obj.get('address_line_1')
          address_line_2 = obj.get('address_line_2')
          city = obj.get('city')
          postal_code = obj.get('postal_code')
      #    qs = Customer.objects.filter(email__iexact=email)
          if password != password2:
              return Response('Passwords Must Match')

          user = Customer(email=email, password=password, username=email
                              , first_name=first_name, last_name=last_name, phone_number=phone_number,
                              address_line_1=address_line_1, address_line_2=address_line_2,
                              city=city, postal_code=postal_code)

          user.is_active = False
          user.save()
          return user

         # if qs.exists():
          #    return Response('User Already Exists')

class CustomerLogInSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Customer
        fields=[
            'email',
            'password',
            'token',
            'expires',
            'id',

        ]
    extra_kwargs = {'password': {'write only': True}}
    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('api-customer:login', kwargs={'id': obj.id}, request=request)

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def get_token(self, obj):  # instance of model
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self,data):
        user_obj = None
        email = data.get('email',None)
        password = data.get('password', None)
        if email is None: #and not username:
            raise serializers.ValidationError('Email is required')
        user=Customer.objects.filter(
            Q(email=email)
               ).distinct()
        if user.exists() and user.count()==1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This email exists ")
        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials ")
        data = data.get_token()
        return data


