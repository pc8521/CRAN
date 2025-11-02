from django.shortcuts import render
from .models import Wishlist

# Create your views here.

def add_to_wishlist(request, product_id):
    wishlist=Wishlist.objects.create(user=request.user, product_id=product_id)        
    wishlist.save()