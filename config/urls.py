from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
import debug_toolbar  
from products import views
#from cart import views 

#from cart.views import add_to_cart, cart, checkout  


urlpatterns = [ 
    path('', include("pages.urls", namespace="pages")),
    path('products/', include("products.urls", namespace="products")),  
    path('stores/', views.store, name='store'),
    #path('contacts/', include("contacts.urls", namespace="contacts")),
    path('accounts/',include("accounts.urls", namespace="accounts")),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    #path('accounts/register/', auth_views.RegisterView.as_view(), name='register'), 
    path('admin/', admin.site.urls),
    path('cart/', include("cart.urls", namespace="cart")), 
    path('orders/', include("orders.urls", namespace="orders")),    
    #path('add_to_cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)                                             
 

# ✅ Only include debug toolbar in development
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

# ✅ Serve media files
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header="Shop Admin"
admin.site.site_title="Shop Admin Portal"
admin.site.index_title="Welcome to Shop Center Admin Portal"






