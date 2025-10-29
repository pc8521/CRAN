from django.shortcuts import render, redirect
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

def register(request):
     return render(request, 'pages/register.html')
def myaccount(request):
    return render(request, 'pages/myaccount.html')

def edit_myaccount(request):
    if request.method == 'POST': 
        user=request.user
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.email=request.POST.get('email')
        user.username=request.POST.get('username')
        user.save()

        return redirect('account')
    return render(request, 'pages/edit_myaccount.html')


 
 


 


