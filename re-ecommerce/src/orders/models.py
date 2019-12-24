import math
from django.db import models
from django.db.models.signals import pre_save, post_save
from Restecommerce.utils import unique_order_id_generator

from decimal import Decimal
from django.conf import settings
from django.db.models.signals import pre_save, post_save
# Create your models here.
from carts.models import Cart
from customers.models import Customer
from products.models import Product


class Order(models.Model):
    order_id = models.CharField(max_length=122, blank=True)
    billing_profile = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products         =models.ManyToManyField(Product)
  #  cart             = models.ForeignKey(Cart, on_delete=models.CASCADE)
  #  status           = models.CharField(max_length=122,default='created',choices=ORDER_STATUS_CHOICES)
    shipping_total   = models.DecimalField(default= 6.00, max_digits=100, decimal_places=2, null=True, blank=True)
    total            = models.DecimalField(default= 0.00, max_digits=100, decimal_places=2, null=True, blank=True)
    active           = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id






def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id= unique_order_id_generator(instance)
   #qs=Order.objects.exclude(billing_profile=instance.billing_profile)
   # if qs.exists():
    #    qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender= Order)


