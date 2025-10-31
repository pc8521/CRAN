from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'products'

urlpatterns = [
    path('products/', views.products, name='products'),  # List view
    path('products/<int:product_id>/', views.product, name='product'),  # Detail view
    path('categories/', views.categories, name='categories'),
    path('search/', views.search, name='search'),
    path('products/category/<int:category_id>/', views.products, name='products_by_category'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('store/', views.store, name='store'),
    #path('product/<int:product_id>', views.product, name='product'),
    #path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]