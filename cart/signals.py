# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from .models import CartItem
# from .utils import get_session_cart, save_session_cart

# @receiver(user_logged_in)
# def merge_cart_on_login(sender, request, user, **kwargs):
#     session_cart = get_session_cart(request)  # 這是 {'18': {'quantity': 1, 'id': '18'}, ...}
#     for product_id, item_data in session_cart.items():
#         # ✅ 正確取出數量
#         quantity = item_data['quantity']
#         item, created = CartItem.objects.get_or_create(
#             user=user,
#             product_id=product_id,
#             defaults={'quantity': quantity}
#         )
#         if not created:
#             item.quantity += quantity
#             item.save()
#     save_session_cart(request, {})  # Clear session cart# 