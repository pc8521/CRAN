from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('myaccount', views.myaccount, name='myaccount'),
    path('reorder/<int:order_id>/', views.reorder, name='reorder'),
]