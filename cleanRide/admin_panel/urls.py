from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("add-product/", views.add_product, name="add_product"),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),

    path('admin/orders/', views.orders_admin, name='orders_admin'),
    path('admin/orders/edit/<int:pk>/', views.admin_edit_order, name='admin_edit_order'),

    path('admin-analytics/', views.admin_analytics, name='admin_analytics'),

    path('blogs/', views.blog, name='blog'),

    path('blogs-details/', views.blog_list, name='blog_list'),
    path('blogs-details/new/', views.blog_create, name='blog_create'),
    path('blogs-details/<int:id>/edit/', views.blog_edit, name='blog_edit'),
    path('blogs-details/<int:id>/', views.blog_detail, name='blog_detail'),
]
