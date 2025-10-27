from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    message = models.TextField()
    type = models.CharField(max_length=50)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} to {self.user.username} about {self.product.name if self.product else 'N/A'}"

    class Meta:
        ordering = ['-sent_at']