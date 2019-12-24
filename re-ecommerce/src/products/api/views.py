from rest_framework.views import Response
from rest_framework import permissions, generics
from rest_framework.views import APIView

from products.models import Product
from products.api.serializers import ProductSerializer

class ProductListAPIView(generics.ListAPIView):
    permission_classes      = []
    authentication_classes  =  []
    serializer_class        = ProductSerializer
    queryset                =Product.objects.all()
    search_fields           =('title',"description",'price' )
   # def get_queryset(self):
    #    qs=Product.objects.all()
     #   query=self.request.GET.get('q')
      #  if query is not None:
       #     qs=qs.filter(title__icontains =query)
       # return qs


class ProductDetailAPIView(generics.RetrieveAPIView):
    permission_classes      = []
    authentication_classes  =  []
    serializer_class        = ProductSerializer
    queryset                = Product.objects.all()
    lookup_field            = 'id'

