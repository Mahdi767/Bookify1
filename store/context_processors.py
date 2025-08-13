# store/context_processors.py
from .models import Cart, CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            item_count = sum(item.quantity for item in cart.items.all())
        except Cart.DoesNotExist:
            item_count = 0
    else:
        item_count = 0
    
    return {'cart_item_count': item_count}