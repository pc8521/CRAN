from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'), #/cart/
    path('checkout/', views.checkout, name='checkout'),  # /cart/checkout/
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),   
]