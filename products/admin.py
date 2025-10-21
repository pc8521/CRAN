from django.contrib import admin
from django import forms
from .models import Product
from .models import Category

# Register your models here.

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 
            'category_img',]

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm

admin.site.register(Category, CategoryAdmin)


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'description', 'price','stock',
            'category', 'is_active', 'tag', 'brand',
            'product_img','product_img1',
            'product_img2',]

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

admin.site.register(Product, ProductAdmin)