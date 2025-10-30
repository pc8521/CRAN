from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from products.models import Product
from stores.models import Store

class Order(models.Model):
    ORDERED='ordered'
    COLLECTED='collected'
    
    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (COLLECTED, 'Collected')
    )
    
    user= models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255,blank=True, null=True)
    last_name=models.CharField(max_length=255,blank=True, null=True)
    email=models.CharField(max_length=255, blank=True, null=True)
    phone=models.CharField(max_length=255, blank=True, null=True)
    store= models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ORDERED')
    order_date = models.DateTimeField(auto_now_add=True)
    
    paid=models.BooleanField(default=False)
    paid_amount=models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.status}"
    
class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField(default=1)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.order