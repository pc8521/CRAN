from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('map', views.map, name='map'),
]
