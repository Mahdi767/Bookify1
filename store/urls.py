# store/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Admin Panel URLs
    path('', views.home, name='home'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/upload/', views.upload_book, name='upload_book'),
    path('admin-panel/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('admin-panel/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'), 
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]