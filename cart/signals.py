# cart/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from .models import CartItem

@receiver(user_logged_in)
def merge_anonymous_cart_to_user(sender, request, user, **kwargs):
    # 直接從 session 讀取購物車資料（不要用 Cart(request)！）
    session_cart = request.session.get(settings.CART_SESSION_ID, {})
    
    if not session_cart:
        return  # 沒有匿名購物車，無需合併

    # 合併到 DB（覆蓋，避免重複累加）
    for product_id, item in session_cart.items():
        CartItem.objects.update_or_create(
            user=user,
            product_id=product_id,
            defaults={'quantity': item['quantity']}
        )

    # 清空 session 購物車（防止重複）
    if settings.CART_SESSION_ID in request.session:
        del request.session[settings.CART_SESSION_ID]
        request.session.modified = True

# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from django.conf import settings
# from .models import CartItem
# from .cart import Cart
# 
# @receiver(user_logged_in)
# def merge_cart_on_login(sender, request, user, **kwargs):
#     # 從 session 建立 Cart 物件（匿名狀態）
#     cart = Cart(request)
#     if not cart.cart:
#         return  # session 購物車為空，無需合併
# 
#     # 合併到 DB（覆蓋，避免累加）
#     for product_id, item in cart.cart.items():
#         CartItem.objects.update_or_create(
#             user=user,
#             product_id=product_id,
#             defaults={'quantity': item['quantity']}
#         )
# 
#     # 清空 session 購物車（避免重複）
#     cart.cart.clear()
#     cart.save()
