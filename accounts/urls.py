# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('clear-orders/', views.clear_completed_orders, name='clear_completed_orders'),
]