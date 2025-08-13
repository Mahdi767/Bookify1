# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from store.models import Order
from django.contrib import messages


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    context = {'orders': orders}
    return render(request, 'accounts/my_orders.html', context)


@login_required
def clear_completed_orders(request):
    if request.method == 'POST':
        Order.objects.filter(user=request.user, is_completed=True).delete()
        messages.success(request, 'Completed orders have been cleared.')
    return redirect('my_orders')