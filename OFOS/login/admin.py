from django.contrib import admin
from .models import CustomeUser,Product,Order,Order_items
admin.site.register(CustomeUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Order_items)
# Register your models here.
