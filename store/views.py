# store/views.py

from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from .models import Book, Cart, CartItem, Order, OrderItem
from .decorators import admin_only
from .forms import BookForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    search_query = request.GET.get('q', '') 

    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )
    else:
        books = Book.objects.all()

    context = {
        'books': books,
        'search_query': search_query 
    }
    return render(request, 'store/home.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    related_books = Book.objects.filter(author=book.author).exclude(pk=pk)[:4]
    context = {
        'book': book,
        'related_books': related_books
    }
    return render(request, 'store/book_detail.html', context)



@login_required 
@admin_only     
def admin_dashboard(request):
    books = Book.objects.all().order_by('-created_at') 
    context = {'books': books}
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@admin_only
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BookForm()

    context = {'form': form}
    return render(request, 'admin_panel/upload_book.html', context)

@login_required
@admin_only
def edit_book(request, pk):
    book_instance = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':

        form = BookForm(request.POST, request.FILES, instance=book_instance)
        
        if form.is_valid():
        
            book_instance.title = form.cleaned_data['title']
            book_instance.author = form.cleaned_data['author']
            book_instance.description = form.cleaned_data['description']
            book_instance.price = form.cleaned_data['price']

          
            if form.cleaned_data['image'] is not None:
         
                if form.cleaned_data['image'] == False:
                 
                    book_instance.image = None
                else:
                
                    book_instance.image = form.cleaned_data['image']
            
        
            book_instance.save()
            
            return redirect('admin_dashboard')
        else:
       
            context = {
                'form': form,
                'book': book_instance
            }
            return render(request, 'admin_panel/edit_book.html', context)

    else:
      
        form = BookForm(instance=book_instance)

    context = {
        'form': form,
        'book': book_instance
    }
    return render(request, 'admin_panel/edit_book.html', context)

@login_required
@admin_only
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('admin_dashboard')

    context = {'book': book}
    return render(request, 'admin_panel/delete_confirm.html', context)



@login_required
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    quantity = int(request.POST.get('quantity', 1)) 
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
        
    cart_item.save()

    messages.success(request, f'"{book.title}" has been added to your cart.')
    
    return redirect('book_detail', pk=pk)


@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all() 
        total_price = sum(item.book.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/cart.html', context)

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def update_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        if not cart_items:
            return redirect('home')
        
        total_price = sum(item.book.price * item.quantity for item in cart_items)

    except Cart.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')

        if not shipping_address:
            context = {
                'cart_items': cart_items,
                'total_price': total_price,
                'error': 'Shipping address is required.'
            }
            return render(request, 'store/checkout.html', context)


        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            shipping_address=shipping_address,
            is_completed=True 
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
    
        cart.items.all().delete()
        return redirect('order_confirmation', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'store/order_confirmation.html', context)