"""
URL configuration for cleanRide project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('admin_panel/', include('admin_panel.urls')),
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('cart', views.view_cart, name="cart"),
    path('contact', views.view_contact, name="contact"),
    path('contact/', views.contact, name='contact'),
    path('about-us/', views.about, name='about'),

    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    path('modify_cart/plus/', views.modify_cart, {'operation': 'plus'}, name='modify_cart_plus'),
    path('modify_cart/minus/', views.modify_cart, {'operation': 'minus'}, name='modify_cart_minus'),
    path('removecart/', views.remove_cart, name='remove_cart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

