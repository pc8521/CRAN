from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    # product_image = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    # session_key=models.CharField(max_length=40, null=True, blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # total = models.DecimalField(max_digits=10, decimal_places=2)

    # class Meta:
    #     unique_together = [
    #         ('user', 'product'),
    #         ('session_key', 'product'),
    #     ]


    #  class Meta:
    #     unique_together = ('user', 'session_key', 'product')
    
    
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
