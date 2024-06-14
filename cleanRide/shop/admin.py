from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse

from admin_panel.models import SubCategory
from .models import Product, CustomUser

from .models import (
 Customer,
 Product,
 Cart,
 OrderPlaced,
 CustomUser
)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')

admin.site.register(CustomUser, CustomUserAdmin)

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    class Media:
        js = ('product_admin.js',)

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

admin.site.register(Product, ProductAdmin)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'customer', 'customer_info', 'product', 'product_info', 'quantity', 'ordered_date', 'status']

  def product_info(self, obj):
   link = reverse("admin:shop_product_change", args=[obj.product.pk])
   return format_html('<a href="{}">{}</a>', link, obj.product.title)

  def customer_info(self, obj):
   link = reverse("admin:shop_customer_change", args=[obj.customer.pk])
   return format_html('<a href="{}">{}</a>', link, obj.customer.name)
 
