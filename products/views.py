from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Category, Product 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from . choices import brand_choices, tag_choices
from django.db.models import Q

# Create your views here.


def products(request):
    products=Product.objects.all().filter(is_active=True)
    paginator=Paginator(products,3) 
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    categories=Category.objects.all()
    context ={"products":paged_products,
            "categories":categories,
            "brand_choices":brand_choices,
            "tag_choices":tag_choices
            } 
    return render(request, 'products/products.html', context)

def product(request, product_id):
    categories=Category.objects.all()
    product=get_object_or_404(Product, pk=product_id) 
    context={
        'categories': categories,
        'brand_choices': brand_choices,
        'tag_choices': tag_choices,
        'product': product
        }
    return render(request, 'products/product.html', context)


def search(request):
    queryset_list=Product.objects.order_by('-price')
    
    keywords=request.GET.get('keywords')
    if keywords:
        queryset_list=queryset_list.filter(
            Q(description__icontains=keywords) |
            Q(category__name__icontains=keywords) |
            Q(name__icontains=keywords) |
            Q(brand__icontains=keywords)
        )
    
    category=request.GET.get('category')
    if category:
        queryset_list=queryset_list.filter(category__name__iexact=category)
    
    brand = request.GET.get('brand')
    if brand:
        queryset_list=queryset_list.filter(brand__iexact=brand)        
            
    tag=request.GET.get('tag')
    if tag:
        queryset_list=queryset_list.filter(tag__iexact=tag)
        
    paginator=Paginator(queryset_list,3) 
    page=request.GET.get('page')
    paged_products=paginator.get_page(page) 
    context={"products":paged_products,
            "categories":Category.objects.all(),
            "brand_choices":brand_choices,
            "tag_choices":tag_choices,        
            "values":request.GET}    
    return render(request, 'products/search.html', context)


def store(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        store_email = request.POST.get('store_email')
        # Handle the form submission here
        return redirect('products:products')  # or wherever you want to go


# def categories(request):
#     categories = Category.objects.all()
#     return render(request, 'pages/categories.html', {'categories': categories})

# def products(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     products = Product.objects.filter(category=category)
#     return render(request, 'products/products_a.html', {'category': category, 'products': products})

# def product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'products/product_a.html', {'product': product})