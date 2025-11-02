from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class Wishlist(models.Model):
    user= models.ForeignKey(User, related_name='wishlist', on_delete=models.CASCADE)
    product= models.ForeignKey(Product, related_name='wishes', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)