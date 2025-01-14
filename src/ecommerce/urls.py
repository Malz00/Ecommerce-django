"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import home_page,about_page,contact_page
from accounts.views import LoginView, RegisterView, guest_register,logout_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from cart.views import cart_detail_api_view
from billing.views import payment_method_view, payment_method_create_view

from django.conf import settings
from django.conf.urls.static import static

from cart.views import cart_home

urlpatterns = [ 
    path('products', include(('product.urls', 'products' ), namespace='products' )),
    path('search', include(('search.urls', 'search' ), namespace='search' )),
    path('cart/', include(('cart.urls', 'cart' ), namespace='cart' )),
    
    path('api/cart', cart_detail_api_view, name='api-cart'),
    path('', home_page, name='home'),
    path('about', about_page, name='about'),
    path('contact', contact_page, name='contact'),
    path('checkout/address/create_view', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/guest/', guest_register, name='guest_register'),
    path('payment/method-createview', payment_method_create_view, name='payment-method-endpoint'),
    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    path('logout/', logout_view, name='logout'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('logout/', LogoutView.as_view(next_page='/custom-page/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('admin/', admin.site.urls),

]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
