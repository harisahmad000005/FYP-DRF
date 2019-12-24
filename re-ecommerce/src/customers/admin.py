from django.contrib import admin
from django.contrib.auth.models import Group,User
# Register your models here.
from .models import Customer
admin.site.site_header = 'Indus Importers and Traders Admin Panel'
class CustomerAdmin(admin.ModelAdmin):
    exclude = [ "username"]


admin.site.register(Customer, CustomerAdmin)



admin.site.unregister(Group)
admin.site.unregister(User)