from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here. 

def register(request): 
    return render(request, 'accounts/register.html')

def login(request): 
    return render(request, 'accounts/login.html')

def logout(request): 
    return HttpResponse("Logout user")

def dashboard(request): 
    return render(request, 'accounts/dashboard.html')