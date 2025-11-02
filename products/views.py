from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Review
from . choices import brand_choices, tag_choices
from cart.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from wishlist.models import Wishlist
from django.contrib.auth.decorators import login_required

# Create your views here.

categories=Category.objects.all()
category_data = {
                "categories":categories,
                "brand_choices":brand_choices,
                "tag_choices":tag_choices
                }

def products(request, category_id=None):
    # Determine category from path or query string
    category_id = category_id or request.GET.get('category')

    # Filter products by category if provided
    if category_id:
        product_list = Product.objects.filter(category_id=category_id)
    else:
        product_list = Product.objects.all()

    # Paginate the filtered product list
    paginator = Paginator(product_list, 3)  # Show 3 products per page
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)

    context = {
        "products": paged_products,
        "category_id": category_id,
        **category_data
    }
    return render(request, 'products/products.html', context)

def product(request, product_id):
    product=get_object_or_404(Product, pk=product_id) 
    context={
            "product":product,
            **category_data,
            }
    if request.method == 'POST':
        rating = request.POST.get('rating', 5)
        content = request.POST.get('content', '')
        
        if content:
            reviews = Review.objects.filter(created_by=request.user, product=product)
            
            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.content = content
                review.save()
            else:
                review=Review.objects.create(
                    product=product,
                    rating=rating,
                    content=content,
                    created_by=request.user
                )
    
            return redirect('products:product', product_id=product.id)
    
    return render(request, 'products/product.html', context)

def categories(request):
    categories = Category.objects.all()
    return render(request, 'products/categories.html', {'categories': categories})

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
            "values":request.GET,
            **category_data
            }    
    return render(request, 'products/search.html', context)

def inquiry(request):
    return render(request, 'products/inquiry.html')


def store(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        store_email = request.POST.get('store_email')
        # Handle the form submission here
        return redirect('products:products')  # or wherever you want to go
    
@login_required 
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist=Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('products:products')  # Redirect back to product page

@login_required 
def delete_wishlist(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    item.delete()
    return redirect('accounts:dashboard')  # 修正：跳回正確的 dashboard

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