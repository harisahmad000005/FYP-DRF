from django.contrib.auth import authenticate,get_user_model
from django.db.models import Q
import datetime
from django.core import serializers

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from  .serializers import CustomerRegisterSerializer,CustomerLogInSerializer,CustomerListSerializer
from  customers.models import Customer

jwt_payload_handler              = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler               = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler     = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


#class UserDetailAPIView(generics.RetrieveAPIView):
 #   queryset         = User.objects.filter(is_active=True)
  #  serializer_class = CustomerDetailSerializer
   # lookup_field     ='email' #id

    #def get_serializer_context(self):
     #   return {'request': self.request}



class CustomerRegisterAPIView(generics.CreateAPIView):
    queryset            = Customer.objects.all()
    serializer_class    = CustomerRegisterSerializer
    permission_classes  = [AllowAny]
    def get_serializer_context(self, *args, **kwargs):
        return {
            'request': self.request }













  #  def post(self,request, *args ,**kwargs):
   #     serializer = self.CustomerRegisterSerializer(data=request.data)
    #    if serializer.is_valid():
     #    serializer.save()
      #   return Response(serializer.data)
       # else:
        #  return Response({'Detail': 'Invalid credentials '})
       #     if request.user.is_authenticated:
        #        return Response({'Detail': 'You Are Already Registered and are Authenticated '})
         #   data=request.data
          #  email     = data.get('email')
           # qs = Customer.objects.filter(
            #    Q(email__iexact=email)
           # )
          #  if qs.exists():
           #      raise serializers.ValidationError('Enter a email already')


          #  password  = data.get('password')
           # password2 = data.get('password2')
        #    if password != password2:
         #       raise serializers.ValidationError('Password must match')


          #  first_name = data.get('first_name')
         #   last_name = data.get('last_name')
          #  phone_number = data.get('phone_number')
           # qs = Customer.objects.filter(
            #    Q(phone_number__iexact=phone_number)
          #  )
           # if qs.exists():
            #    raise serializers.ValidationError('Enter a Valid Phone Number')

         #   address_line_1 = data.get('address_line_1')
          #  address_line_2 = data.get('address_line_2')
           # city = data.get('city')
         #   postal_code = data.get('postal_code')

          #  user=Customer.objects.create(email=email,password=password
           #             ,first_name=first_name,last_name=last_name,phone_number=phone_number,
            #                                 address_line_1=address_line_1,address_line_2=address_line_2,
             #                                city=city,postal_code=postal_code)

           # user.is_active = False
          #  user.save()
          #  return user
          #  payload = jwt_payload_handler(user)
         #   token = jwt_encode_handler(payload)
        #    response = jwt_response_payload_handler(user, request=request)
           # return Response()

                #return Response({'detail': 'You are Successfully Registered '},response)

            #return Response({'detail':'Invalid Request'})

class CustomerAuthAPIView(APIView):
    permission_classes  = [AllowAny]
    authentication_classes = []
    serializer_class    = CustomerLogInSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'Detail': 'You Are Logged in'})
        data = request.data
        email= data.get('email')
        password = data.get('password')
        qs = Customer.objects.filter(
            Q(email__iexact=email) ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if password == user_obj.password:
                user = user_obj
                address = {"email": user.email,"first_name": user.first_name,"last_name": user.last_name,"address_line_1": user.address_line_1,"address_line_2": user.address_line_2,
                             "city": user.city, "postal_code": user.postal_code}
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, address)
                response={"token": token, "email": user.email,"first_name": user.first_name,"last_name": user.last_name, "address_line_1": user.address_line_1,
                 "address_line_2": user.address_line_2,
                 "city": user.city, "postal_code": user.postal_code}
                return Response( response)

               # return Response(response)
        return Response({'detail': 'Invalid Credentials'})






JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
   # 'rest_framework_jwt.utils.jwt_response_payload_handler',
     'accounts.api.utils.jwt_response_payload_handler',

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=5),

    'JWT_AUTH_HEADER_PREFIX': 'Token', #Authoriazation : JWT <token>
    'JWT_AUTH_COOKIE': None,

}