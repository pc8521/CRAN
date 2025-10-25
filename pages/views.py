from django.shortcuts import render
from products.models import Product, Category
from products.choices import brand_choices, tag_choices

# Homepage view
def index(request):                                                                  
    products = Product.objects.filter(stock__gt=0)[:3]
    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories,
        "brand_choices": brand_choices,
        "tag_choices": tag_choices,
    }

    return render(request, 'pages/index.html', context)

def categories(request):
    categories = Category.objects.all()
    return render(request, 'pages/categories.html', {'categories': categories})

def signup(request):
     return render(request, 'pages/signup.html')


