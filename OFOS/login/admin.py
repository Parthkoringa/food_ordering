from django.contrib import admin
from .models import CustomeUser,Product,Order
admin.site.register(CustomeUser)
admin.site.register(Product)
admin.site.register(Order)
# Register your models here.
