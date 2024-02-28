from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomeUser(AbstractUser):
    contact= models.CharField(max_length=10)
    address = models.TextField(max_length=200)
    def __str__(self):
        return self.username
    
    
class Product(models.Model):
    p_name = models.CharField(max_length=20)
    p_description = models.TextField(max_length=200)
    unit_price = models.IntegerField()
    p_image = models.ImageField()
    def __str__(self):
        return self.p_name
    

class Order(models.Model):
    order_date = models.DateTimeField()
    r_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amt = models.IntegerField()
    order_status = models.CharField(max_length=3)
    
    def __str__(self):
        return "order" 
        
        
# class Bill(models.Model):
#     o_id = models.ForeignKey(Order, on_delete = models.CASCADE)
#     p_id = models.ForeignKey(Product, on_delete = models.CASCADE)
#     qty = Order.quantity
#     date_time = Order.order_date
#     total_amt = Order.total_amt
#     def __str__(self):
#         return self.id
    