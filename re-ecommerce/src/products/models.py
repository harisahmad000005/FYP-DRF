from django.db.models import Q
import random
import os
from Restecommerce.utils import unique_slug_generator
from django.db import models
from django.db.models.signals import pre_save

from django.urls import reverse




def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    print(instance)
    print(filename)

    new_filname =random.randint(0,334252312)
    name, ext   = get_filename_ext(filename)
    final_filename= '{new_filname}{ext}'.format(new_filname=new_filname, ext= ext)
    return 'products/{new_filname}/{final_filename}'.format(new_filname= new_filname, final_filename= final_filename)


class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)


class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return self.get_queryset().active()




class Product(models.Model):
    title       = models.CharField(max_length=120,unique= True)
    description = models.TextField(blank=False)
    price       = models.DecimalField(decimal_places= 2, max_digits=20, default=39.99)
    image       = models.ImageField(upload_to= upload_image_path, null=False, blank = False)
    featured    = models.BooleanField(default= False )
    active      = models.BooleanField(default= True )
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'products'

    objects = ProductManager()


    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def get_absolute_url(self):
         # return "/products/{slug}".format(slug=self.slug)
        return reverse('products:detail', kwargs={'slug': self.slug})



#def product_pre_save_receiver (sender , instance, *args ,**kwargs):
  #  if not instance.slug:
 #       instance.slug =unique_slug_generator(instance)

#pre_save.connect(product_pre_save_receiver, sender= Product)
