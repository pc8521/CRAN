

from django.urls import path
from . import views # import views.py in the same directory

app_name = 'pages'

urlpatterns = [
   path('', views.index, name='index'),
   path('categories/', views.categories, name='categories'),
   path('myaccount/', views.myaccount, name='myaccount'),
   path('edit_myaccount/', views.edit_myaccount, name='edit_myaccount'),
   
   
]