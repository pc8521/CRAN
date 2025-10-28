from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from products.models import Product

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
    return render(request, 'cart/cart.html')

def update_Cart(request, product_id, action):
    cart=Cart(request)
     
    if action == 'increment':
        cart.add(product_id,1,True)
    else:
        cart.add(product_id,-1, True)
        
        product=Product.objects.get(pk=product_id)
        quantity=cart.get_item(product_id)
        
    product = Product.objects.get(pk=product_id)
    quantity=cart.get_item(product_id)
     
    item = {
        'product': {
            'id': product.id,
            'name': product.name,
            'image': product.image,
        },
        'total_price': (quantity * product.price), 
        'quantity': quantity,   
    }
    
    response = render(request, 'cart/partials/cart_item.html',{'item': item})
    response['HX-Trigger']='update-menu-cart'
    return response
    
    
   
   
@login_required
def checkout(request):
    return render(request, 'cart/checkout.html')




def hx_menu_cart(request):
    return render(request, 'cart/menu_cart.html')




def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    grand_total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.price * quantity
        items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price
        })
        grand_total += total_price

    cart_count = len(cart)  # Unique product count
    return render(request, 'cart.html', {
        'items': items,
        'grand_total': grand_total,
        'cart_count': cart_count
    })

def update_cart(request, product_id):
    action = request.POST.get('action')
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if action == 'increment':
        cart[product_id_str] = cart.get(product_id_str, 0) + 1
    elif action == 'decrement':
        if cart.get(product_id_str, 0) > 1:
            cart[product_id_str] -= 1
        else:
            cart.pop(product_id_str, None)

    request.session['cart'] = cart
    return redirect('cart')
