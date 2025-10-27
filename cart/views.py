from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .cart import Cart

# Create your views here.

# def add_to_cart(request, product_id):
#     cart=Cart(request)
#     cart.add(product_id)
#     return render(request, "cart/menu_cart.html")

def add_to_cart(request, product_id):
    print("HTMX request received")  # Add this line
    cart = Cart(request)
    cart.add(product_id)

    if request.htmx:
        # Return only the cart count badge
        return render(request, "cart/partials/cart_count.html", {'cart': cart})
    
    # Fallback for non-HTMX requests
    return render(request, "cart/menu_cart.html", {'cart': cart})


def cart(request):
    cart=Cart(request)

    print(cart)
    for item in cart:
        print(item)
    return render(request, 'cart/cart.html')

@login_required
def checkout(request):
    return render(request, 'cart/checkout.html')

def checkout(request):
    return render(request, 'cart/checkout.html')