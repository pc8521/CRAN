from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from products.models import Category, Product
from products.choices import brand_choices, tag_choices
from django.core.mail import send_mail
from cart.models import CartItem
from orders.models import Order, OrderItem
from wishlist.models import Wishlist

products = Product.objects.select_related('category').all()
categories = Category.objects.all()
Category_data = {
        'categories': categories,
        'brand_choices': brand_choices,
        'tag_choices': tag_choices,
        'products': products,
    }

def register(request): 
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html', {'first_name': first_name, 'last_name': last_name, 'username': username, 'email': email})
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'accounts/register.html', {'first_name': first_name, 'last_name': last_name, 'username': username, 'email': email})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/register.html', {'first_name': first_name, 'last_name': last_name, 'username': username, 'email': email})

        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email, 
            first_name=first_name, 
            last_name=last_name
        )
        user.save()
        # Send email
        send_mail(
            "Registration for " + user.get_full_name(),
            "There has been a registration for " + user.get_full_name() + ". Sign and enjoy shopping.",
            "cranerb7@gmail.com",
            [user.email],
            fail_silently=False,
        )
        messages.success(request, 'You are now registered and can log in')
        return redirect('accounts:login')
    else:
        return render(request, 'accounts/register.html', Category_data)

def login(request): 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('pages:home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html', Category_data)
    
def myaccount(request):
    return render(request, 'accounts/myaccount.html', Category_data)

@require_POST
def logout(request): 
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('pages:home')

@login_required
def dashboard(request):
    cartitems=CartItem.objects.filter(user_id=request.user.id)
    orders=Order.objects.filter(user_id=request.user.id)
    # 1a. Get order items for the current user, sorted by order_id
    orderitems = (
        OrderItem.objects.select_related('order', 'product').filter(order__user=request.user).order_by('order_id')
    )
    # 1b. Get wishlist items for the current user
    wishlist=Wishlist.objects.select_related('user','product').filter(user_id=request.user.id)    
    # 2. Pass grouped data to the template         
    context={
            "cartitems":cartitems,
            "orders":orders,
            "orderitems":orderitems,
            "wishlist":wishlist,
            **Category_data
    }
    return render(request, 'accounts/dashboard.html', context)