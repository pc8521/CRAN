from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from products.models import Category, Product
from products.choices import brand_choices, tag_choices

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
        messages.success(request, 'You are now registered and can log in')
        return redirect('accounts:login')
    else:
        return render(request, 'accounts/register.html')

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
        return render(request, 'accounts/login.html')

@require_POST
def logout(request): 
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('pages:home')

@login_required
def dashboard(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'brand_choices': brand_choices,
        'tag_choices': tag_choices,
        'products': products,
    }
    return render(request, 'accounts/dashboard.html', context)