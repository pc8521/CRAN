from django.shortcuts import render, redirect
from products.models import Category, Product
from products.choices import brand_choices, tag_choices

# Create your views here. 

product=Product.objects.all().filter(is_active=True).order_by('-id')[:3]
categories=Category.objects.all()
context={
        'categories': categories,
        'brand_choices': brand_choices,
        'tag_choices': tag_choices,
        'products': product
        }

def index(request):
    return render(request, 'pages/index.html', context)

def home(request):
    return render(request, 'pages/home.html', context)

def about(request):
    return render(request, 'pages/about.html', context)

def map(request):
    return render(request, 'pages/map.html', context)