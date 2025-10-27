from django.db import models
from datetime import datetime
from django.urls import reverse
from . choices import brand_choices, tag_choices

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20) 
    description = models.TextField(max_length=1000)
    category_img = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True, null=True, default='products/default.jpg')
    
    
    
    # def get_absolute_url(self):
    #     return reverse('products', args=[str(self.id)])
    def __str__(self):
        return self.name
    

TAG = [
    ("New", "🆕 New"),
    ("Sale", "🔥 Sale"),
    ("Featured", "⭐ Featured"),
    ("Limited", "⏳ Limited"),
    ("Classic", "🎩 Classic"), 
]

class Product(models.Model):
    sku = models.TextField(max_length=20)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    tag = models.CharField(max_length=20, choices=tag_choices.items())
    brand = models.CharField(max_length=20, choices=brand_choices.items())
    product_img = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True, null=True, default='products/default.jpg')
    product_img1 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True, null=True, default='products/default.jpg')
    product_img2 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True, null=True, default='products/default.jpg')

    
    def __str__(self):      
        return f"{self.name} - {self.category}"