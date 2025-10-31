from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from products.models import Product
from products.models import Category
from products.choices import brand_choices, tag_choices

products = Product.objects.select_related('category').all()
categories = Category.objects.all()
categories_data = {
        'categories': categories,
        'brand_choices': brand_choices,
        'tag_choices': tag_choices,
        'products': products,
        }

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return render(request, "cart/menu_cart.html", {'cart': cart})

def cart(request):
    return render(request, 'cart/cart.html', categories_data)

def update_cart(request, product_id, action):
    cart = Cart(request)

    if action == 'increment':
        cart.add(product_id, 1, True)
    else:
        cart.add(product_id, -1, True)

    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)
    
    if quantity:
        quantity = quantity['quantity']
    

        item = {
            'product': product,
            'total_price': (quantity * product.price),
            'quantity': quantity,
        }
    
    else:
        item = None 
        
    response = render(request, 'cart/partials/cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'
    return response   

# @login_required

def checkout(request):
    cart = Cart(request)
    context = {
        'cart': cart,
        'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
        **categories_data
    }
    return render(request, 'cart/checkout.html', context)

def hx_menu_cart(request):
    return render(request, 'cart/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')