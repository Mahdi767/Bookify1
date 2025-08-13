# store/admin.py
from django.contrib import admin
from .models import Book, Cart, CartItem, Order, OrderItem

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'created_at')
    search_fields = ('title', 'author')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # Don't show extra empty forms

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'order_date', 'is_completed')
    list_filter = ('is_completed', 'order_date')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]

# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)