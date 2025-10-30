from .models import CartItem

def get_session_cart(request):
    return request.session.get('cart', {})

def save_session_cart(request, cart_data):
    request.session['cart'] = cart_data
    request.session.modified = True

def merge_session_cart_to_user(request):
    if request.user.is_authenticated:
        session_cart = get_session_cart(request)
        for product_id, quantity in session_cart.items():
            item, created = CartItem.objects.get_or_create(
                user=request.user,
                product_id=product_id,
                defaults={'quantity': quantity}
            )
            if not created:
                item.quantity += quantity
                item.save()
        save_session_cart(request, {})  # Clear session cart after merge