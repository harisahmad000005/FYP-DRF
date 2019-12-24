from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class CustomerQuerySet(models.QuerySet):
    pass

class CustomerManager(models.Manager):
    def get_address(self, request):
        user =self.request.user
        return '{line1},{line2},\n{city},\n{postal}'.format(
            line2=self.address_line_2,
            line1=self.address_line_1,
            city=self.city,
            postal=self.postal)




class Customer(models.Model):
    username = models.CharField(max_length=10, null=True, blank=True)
    first_name     = models.CharField(max_length=10,null=False, blank=False)
    last_name      = models.CharField(max_length=15,null=False, blank=False)
    email          = models.EmailField(null=False, blank=False, unique=True)
    password       = models.CharField(max_length=10)
    phone_number   = models.CharField(max_length=11,unique=True,null=False, blank=False)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city           = models.CharField(max_length=120)
    postal_code    = models.CharField(max_length=120)

    objects = CustomerManager()
    def __str__(self):
        return self.email


