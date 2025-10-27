from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from products.models import Product
from stores.models import Store

# Create your models here.

class Order(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    store= models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.status}"
    
class Orderitem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order= models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.order
    

    