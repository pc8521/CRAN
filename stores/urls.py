from django.urls import path
from . import views


app_name = 'stores'

# urls.py
path('store/', views.store_view, name='store')

