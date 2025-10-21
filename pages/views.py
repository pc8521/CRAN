from django.shortcuts import render, redirect
from products.models import Category, Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from products.choices import brand_choices, tag_choices
from django.db.models import Q

# Create your views here. 

product=Product.objects.filter(is_active=True)[:3]
categories=Category.objects.all()
context={
        'categories': categories,
        'brand_choices': brand_choices,
        'tag_choices': tag_choices,
        'products': product
        }

def index(request):
    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html', context)